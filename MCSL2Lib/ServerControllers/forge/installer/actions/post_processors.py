"""
/*
 * Copyright (c) Forge Development LLC
 * SPDX-License-Identifier: LGPL-2.1-only
 */
package net.minecraftforge.installer.actions;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Supplier;
import java.util.jar.Attributes;
import java.util.jar.JarFile;
import java.util.stream.Collectors;

import javax.net.ssl.SSLException;
import javax.swing.JOptionPane;

import net.minecraftforge.installer.DownloadUtils;
import net.minecraftforge.installer.SimpleInstaller;
import net.minecraftforge.installer.actions.ProgressCallback.MessagePriority;
import net.minecraftforge.installer.json.Artifact;
import net.minecraftforge.installer.json.Install.Processor;
import net.minecraftforge.installer.json.InstallV1;
import net.minecraftforge.installer.json.Version.Library;
import net.minecraftforge.installer.json.Util;

public class PostProcessors {
    private final InstallV1 profile;
    private final boolean isClient;
    private final ProgressCallback monitor;
    private final boolean hasTasks;
    private final List<Processor> processors;

    public PostProcessors(InstallV1 profile, boolean isClient, ProgressCallback monitor) {
        this.profile = profile;
        this.isClient = isClient;
        this.monitor = monitor;
        this.processors = profile.getProcessors(isClient ? "client" : "server");
        this.hasTasks = !this.processors.isEmpty();
    }

    public Library[] getLibraries() {
        return hasTasks ? profile.getLibraries() : new Library[0];
    }

    public int getTaskCount() {
        return hasTasks ? 0 :
            profile.getLibraries().length +
            processors.size() +
            profile.getData(isClient).size();
    }

    public Set<File> process(File librariesDir, File minecraft, File root, File installer) {
        try {
            Map<String, DataEntry> data = loadData(librariesDir);
            if (data == null)
                return null;

            data.put("SIDE",              new DataEntry(isClient ? "client" : "server"));
            data.put("MINECRAFT_JAR",     new FileEntry(minecraft));
            data.put("MINECRAFT_VERSION", new DataEntry(profile.getMinecraft()));
            data.put("ROOT",              new FileEntry(root));
            data.put("INSTALLER",         new FileEntry(installer));
            data.put("LIBRARY_DIR",       new FileEntry(librariesDir));

            if (processors.size() == 1)
                monitor.stage("Building Processor");
            else
                monitor.start("Building Processors");

            List<List<Output>> allOutputs = buildOutputs(librariesDir, data, processors);
            if (allOutputs == null)
                return null;

            String libPrefix = librariesDir.getAbsolutePath().replace('\\', '/');
            if (!libPrefix.endsWith("/"))
                libPrefix += '/';

            Set<File> ret = new HashSet<>();
            for (int x = 0; x < processors.size(); x++) {
                monitor.progress((double)(x + 1) / processors.size());
                log("===============================================================================");
                Processor proc = processors.get(x);
                List<Output> outputs = allOutputs.get(x);

                if (!outputs.isEmpty()) {
                    boolean miss = false;
                    log("  Cache: ");
                    for (Output output : outputs) {
                        if (!output.file.exists()) {
                            log("    " + output.file + " Missing");

                            String path = output.file.getAbsolutePath().replace('\\', '/');
                            if (!path.startsWith(libPrefix)) {
                                miss = true;
                            } else {
                                String relative = "/cache/" + path.substring(libPrefix.length());
                                try (final InputStream input = DownloadUtils.class.getResourceAsStream(relative)) {
                                    if (input != null) {
                                        log("    Extracting output from " + relative);
                                        if (!output.file.getParentFile().exists())
                                             output.file.getParentFile().mkdirs();

                                        Files.copy(input, output.file.toPath(), StandardCopyOption.REPLACE_EXISTING);
                                        String sha1 = DownloadUtils.getSha1(output.file);
                                        if (output.sha1.equals(sha1)) {
                                            log("      Extraction completed: Checksum validated.");
                                            ret.add(output.file);
                                        } else {
                                            log("    " + output.file);
                                            log("      Expected: " + output.sha1);
                                            log("      Actual:   " + sha1);
                                            miss = true;
                                            output.file.delete();
                                        }
                                    } else {
                                        miss = true;
                                    }
                                } catch (IOException e) {
                                    e.printStackTrace();
                                    return null;
                                }
                            }
                        } else {
                            String sha = DownloadUtils.getSha1(output.file);
                            if (sha.equals(output.sha1)) {
                                log("    " + output.file + " Validated: " + output.sha1);
                                ret.add(output.file);
                            } else {
                                log("    " + output.file);
                                log("      Expected: " + output.sha1);
                                log("      Actual:   " + sha);
                                miss = true;
                                output.file.delete();
                            }
                        }
                    }

                    if (!miss) {
                        log("  Cache Hit!");
                        continue;
                    }
                }

                File jar = proc.getJar().getLocalPath(librariesDir);
                if (!jar.exists() || !jar.isFile()) {
                    error("  Missing Jar for processor: " + jar.getAbsolutePath());
                    return null;
                }

                // Locate main class in jar file
                JarFile jarFile = new JarFile(jar);
                String mainClass = jarFile.getManifest().getMainAttributes().getValue(Attributes.Name.MAIN_CLASS);
                jarFile.close();

                if (mainClass == null || mainClass.isEmpty()) {
                    error("  Jar does not have main class: " + jar.getAbsolutePath());
                    return null;
                }
                monitor.message("  MainClass: " + mainClass, MessagePriority.LOW);

                List<URL> classpath = new ArrayList<>();
                StringBuilder err = new StringBuilder();
                monitor.message("  Classpath:", MessagePriority.LOW);
                monitor.message("    " + jar.getAbsolutePath(), MessagePriority.LOW);
                classpath.add(jar.toURI().toURL());
                for (Artifact dep : proc.getClasspath()) {
                    File lib = dep.getLocalPath(librariesDir);
                    if (!lib.exists() || !lib.isFile())
                        err.append("\n  ").append(dep.getDescriptor());
                    classpath.add(lib.toURI().toURL());
                    monitor.message("    " + lib.getAbsolutePath(), MessagePriority.LOW);
                }
                if (err.length() > 0) {
                    error("  Missing Processor Dependencies: " + err.toString());
                    return null;
                }

                List<String> args = new ArrayList<>();
                for (String arg : proc.getArgs()) {
                    char start = arg.charAt(0);
                    char end = arg.charAt(arg.length() - 1);

                    if (start == '[' && end == ']') //Library
                        args.add(Artifact.from(arg.substring(1, arg.length() - 1)).getLocalPath(librariesDir).getAbsolutePath());
                    else
                        args.add(Util.replaceTokens(data, arg));
                }
                if (err.length() > 0) {
                    error("  Missing Processor data values: " + err.toString());
                    return null;
                }
                monitor.message("  Args: " + args.stream().map(a -> a.indexOf(' ') != -1 || a.indexOf(',') != -1 ? '"' + a + '"' : a).collect(Collectors.joining(", ")), MessagePriority.LOW);

                ClassLoader cl = new URLClassLoader(classpath.toArray(new URL[classpath.size()]), getParentClassloader());
                // Set the thread context classloader to be our newly constructed one so that service loaders work
                Thread currentThread = Thread.currentThread();
                ClassLoader threadClassloader = currentThread.getContextClassLoader();
                currentThread.setContextClassLoader(cl);
                try {
                    Class<?> cls = Class.forName(mainClass, true, cl);
                    Method main = cls.getDeclaredMethod("main", String[].class);
                    main.invoke(null, (Object)args.toArray(new String[args.size()]));
                } catch (InvocationTargetException ite) {
                    Throwable e = ite.getCause();
                    handleError(e);
                    return null;
                } catch (Throwable e) {
                    handleError(e);
                    return null;
                } finally {
                    // Set back to the previous classloader
                    currentThread.setContextClassLoader(threadClassloader);
                }

                if (!outputs.isEmpty()) {
                    for (Output output : outputs) {
                        ret.add(output.file);
                        if (!output.file.exists()) {
                            err.append("\n    ").append(output.file).append(" missing");
                        } else {
                            String sha = DownloadUtils.getSha1(output.file);
                            if (sha.equals(output.sha1)) {
                                log("  Output: " + output.file + " Checksum Validated: " + sha);
                            } else {
                                err.append("\n    ").append(output.file)
                                   .append("\n      Expected: ").append(output.sha1)
                                   .append("\n      Actual:   ").append(sha);
                                if (!SimpleInstaller.debug && !output.file.delete())
                                    err.append("\n      Could not delete file");
                            }
                        }
                    }
                    if (err.length() > 0) {
                        error("  Processor failed, invalid outputs:" + err.toString());
                        return null;
                    }
                }
            }

            return ret;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    private void handleError(Throwable e) {
        e.printStackTrace();
        StringBuilder buf = new StringBuilder();
        buf.append("Failed to run processor: ").append(e.getClass().getName());
        if (e.getMessage() != null)
            buf.append(':').append(e.getMessage());
        if (e instanceof SSLException) {
            buf.append("\nThis is a SSL Exception, this might be caused by you having an outdated java install.")
                .append("\nTry updating your java before trying again.");
        }
        buf.append("\nSee log for more details");
        error(buf.toString());
        if (e.getMessage() == null)
            error("Failed to run processor: " + e.getClass().getName() + "\nSee log for more details.");
        else
            error("Failed to run processor: " + e.getClass().getName() + ":" + e.getMessage() + "\nSee log for more details.");

    }

    private void error(String message) {
        if (!SimpleInstaller.headless)
            JOptionPane.showMessageDialog(null, message, "Error", JOptionPane.ERROR_MESSAGE);
        for (String line : message.split("\n"))
            monitor.message(line);
    }

    private void log(String message) {
        for (String line : message.split("\n"))
            monitor.message(line);
    }

    private static boolean clChecked = false;
    private static ClassLoader parentClassLoader = null;
    @SuppressWarnings("unused")
    private synchronized ClassLoader getParentClassloader() { //Reflectively try and get the platform classloader, done this way to prevent hard dep on J9.
        if (!clChecked) {
            clChecked = true;
            if (!System.getProperty("java.version").startsWith("1.")) { //in 9+ the changed from 1.8 to just 9. So this essentially detects if we're <9
                try {
                    Method getPlatform = ClassLoader.class.getDeclaredMethod("getPlatformClassLoader");
                    parentClassLoader = (ClassLoader)getPlatform.invoke(null);
                } catch (NoSuchMethodException | IllegalAccessException | IllegalArgumentException | InvocationTargetException e) {
                    log("No platform classloader: " + System.getProperty("java.version"));
                }
            }
        }
        return parentClassLoader;
    }

    private Map<String, DataEntry> loadData(File librariesDir) throws IOException {
        Map<String, String> cfg = profile.getData(isClient);
        if (cfg.isEmpty())
            return new HashMap<>();

        Map<String, DataEntry> ret = new HashMap<>();

        StringBuilder err = new StringBuilder();
        Path temp  = Files.createTempDirectory("forge_installer");
        monitor.start("Created Temporary Directory: " + temp);

        double steps = cfg.size();
        int progress = 1;
        for (String key : cfg.keySet()) {
            monitor.progress(progress++ / steps);
            String value = cfg.get(key);

            DataEntry entry = null;
            if (value.charAt(0) == '[' && value.charAt(value.length() - 1) == ']') { //Artifact
                Artifact artifact = Artifact.from(value.substring(1, value.length() - 1));
                entry = new ArtifactEntry(artifact, librariesDir);
            } else if (value.charAt(0) == '\'' && value.charAt(value.length() - 1) == '\'') { //Literal
                entry = new DataEntry(value.substring(1, value.length() - 1));
            } else {
                File target = Paths.get(temp.toString(), value).toFile();
                monitor.message("  Extracting: " + value);
                if (!DownloadUtils.extractFile(value, target))
                    err.append("\n  ").append(value);

                entry = new FileEntry(target);
            }
            ret.put(key, entry);
        }

        if (err.length() > 0) {
            error("Failed to extract files from archive: " + err.toString());
            return null;
        }

        return ret;
    }

    private List<List<Output>> buildOutputs(File librariesDir, Map<String, DataEntry> data, List<Processor> processors) {
        List<List<Output>> ret = new ArrayList<>();
        for (Processor proc : processors) {
            Map<String, String> outputs = proc.getOutputs();
            if (outputs.isEmpty()) {
                ret.add(Collections.emptyList());
                continue;
            }

            List<Output> pout = new ArrayList<>();
            for (String key : outputs.keySet()) {
                char start = key.charAt(0);
                char end = key.charAt(key.length() - 1);

                String file = null;
                if (start == '[' && end == ']')
                    file = Artifact.from(key.substring(1, key.length() - 1)).getLocalPath(librariesDir).getAbsolutePath();
                else
                    file = Util.replaceTokens(data, key);

                String value = outputs.get(key);
                if (value != null)
                    value = Util.replaceTokens(data, value);

                if (key == null || value == null) {
                    error("  Invalid configuration, bad output config: [" + key + ": " + value + "]");
                    return null;
                }

                pout.add(new Output(new File(file), value));
            }
            ret.add(pout);
        }
        return ret;
    }

    private static class DataEntry implements Supplier<String> {
        protected final String value;
        protected DataEntry(String value) {
            this.value = value;
        }

        @Override
        public String toString() {
            return value;
        }

        @Override
        public String get() {
            return toString();
        }
    }

    private static class FileEntry extends DataEntry {
        @SuppressWarnings("unused")
        private final File file;
        protected FileEntry(File file) {
            super(file.getAbsolutePath());
            this.file = file;
        }
    }

    private static class ArtifactEntry extends DataEntry {
        @SuppressWarnings("unused")
        private final Artifact artifact;
        protected ArtifactEntry(Artifact artifact, File root) {
            super(artifact.getLocalPath(root).getAbsolutePath());
            this.artifact = artifact;
        }
    }

    private static class Output {
        private final File file;
        private final String sha1;

        private Output(File file, String sha1) {
            this.file = file;
            this.sha1 = sha1;
        }
    }
}
"""
import tempfile
import traceback
from pathlib import Path
from typing import List, Set, Dict, Optional

from .progress_callback import ProgressCallback
from ..download_utils import DownloadUtils
from ..java2python import Supplier
from ..json.artifact import Artifact
from ..json.installV1 import InstallV1
from ..json.util import Util
from ..json.version import Version


class PostProcessors:
    profile: InstallV1
    isClient: bool
    monitor: ProgressCallback
    hasTasks: bool = False
    processors: List[InstallV1.Processor]

    class __DataEntry(Supplier[str]):
        value: str

        def __init__(self, value: str):
            super().__init__(self)
            self.value = value

        def __str__(self):
            return self.value

        def get(self):
            return self.value

    class __ArtifactEntry(__DataEntry):
        artifact: Artifact

        def __init__(self, artifact: Artifact, root: Path):
            super().__init__(str(artifact.getLocalPath(root).absolute()))
            self.artifact = artifact

    class __FileEntry(__DataEntry):
        file: Path

        def __init__(self, file: Path):
            super().__init__(str(file.absolute()))
            self.file = file

    class __Output:
        file: Path
        sha1: str

        def __init__(self, file: Path, sha1: str):
            self.file = file
            self.sha1 = sha1

    def __init__(self, profile: InstallV1, isClient: bool, monitor: ProgressCallback):
        self.profile = profile
        self.isClient = isClient
        self.monitor = monitor
        self.processors = profile.getProcessors("client" if isClient else "server")
        self.hasTasks = len(self.processors) > 0

    def getLibraries(self) -> List[Version.Library]:
        return self.profile.getLibraries() if self.hasTasks else []

    def getTaskCount(self) -> int:
        return 0 if self.hasTasks else len(self.profile.getLibraries()) + len(self.processors) + len(
            self.profile.getData(self.isClient))

    def process(self, librariesDir: Path, minecraft: Path, root: Path, installer: Path) -> Optional[Set[Path]]:
        data = self.__loadData(librariesDir)
        if data is None:
            return None
        data.update({
            "SIDE": PostProcessors.__DataEntry("client" if self.isClient else "server"),
            "MINECRAFT_JAR": PostProcessors.__FileEntry(minecraft),
            "MINECRAFT_VERSION": PostProcessors.__DataEntry(self.profile.getMinecraft()),
            "ROOT": PostProcessors.__FileEntry(root),
            "INSTALLER": PostProcessors.__FileEntry(installer),
            "LIBRARY_DIR": PostProcessors.__FileEntry(librariesDir),
        })

        if len(self.processors) == 1:
            self.monitor.stage("Building Processor")
        else:
            self.monitor.stage("Building Processors")

        allOutputs = self.buildOutputs(librariesDir, data)
        if allOutputs is None:
            return None

        libPrefix = librariesDir.absolute()

        rv = set()
        for x in range(len(self.processors)):
            self.monitor.progress((x + 1) / len(self.processors))
            self.log("===============================================================================")
            proc = self.processors[x]
            outputs = allOutputs[x]

            if len(outputs) > 0:
                miss = True
                self.log("  Cache: ")
                for output in outputs:
                    if not output.file.exists():
                        self.log(f"    {output.file} Missing")
                        miss = False

                        if not (outputFile := str(output.file.absolute())).startswith(str(libPrefix)):
                            miss = True
                        else:
                            suffix = outputFile[len(str(libPrefix)):].replace("\\", "/")
                            if suffix.startswith("/"):
                                suffix = suffix[1:]

                            relative = f'./cache/{suffix}'

                            inputPath = Path(relative)
                            if not inputPath.exists():
                                miss = True
                            else:
                                try:
                                    input_ = inputPath.read_bytes()

                                    self.log("    Extracting output from " + relative)
                                    if not (parent := output.file.parent).exists():
                                        parent.mkdir(parents=True)

                                    with open(str(output.file.absolute()), "wb") as fileOutput:
                                        fileOutput.write(input_)
                                    sha1 = DownloadUtils.getSha1(output.file)
                                    if sha1 == output.sha1:
                                        self.log("      Extraction completed: Checksum validated.")
                                        rv.add(output.file)
                                    else:
                                        self.log(f"    {output.file}")
                                        self.log("      Expected: " + output.sha1)
                                        self.log("      Actual:   " + sha1)
                                        miss = True
                                        output.file.unlink(missing_ok=True)
                                except IOError as e:
                                    traceback.print_exception(e)
                                    return None

                    else:
                        sha_ = DownloadUtils.getSha1(output.file)
                        if sha_ == output.sha1:
                            self.log(f"    {output.file} Validated: {output.sha1}")
                            rv.add(output.file)
                        else:
                            self.log(f"    {output.file}")
                            self.log("      Expected: " + output.sha1)
                            self.log("      Actual:   " + sha_)
                            miss = True
                            output.file.unlink(missing_ok=True)

                if not miss:
                    self.log("  Cache Hit!")
                    continue

            jar = proc.getJar().getLocalPath(librariesDir)
            if not jar.exists() or not jar.is_file():
                self.error(f"  Missing Jar for processor: {jar.absolute()}")
                return None

            # Locate main class in jar file
            mainClass = DownloadUtils.getMainClass(jar)
            if not mainClass:  # mainClass is not None or !=""
                self.error(f"  Jar does not have main class: {jar.absolute()}")
                return None
            self.monitor.message(f"  MainClass: {mainClass}")

            classpath: List[Path] = []
            err = ""
            self.monitor.message("  Classpath:")
            self.monitor.message(f"    {jar.absolute()}")
            classpath.append(jar)
            for dep in proc.getClasspath():
                lib = dep.getLocalPath(librariesDir)
                if not lib.exists() and lib.is_file():
                    err += f"\n  {dep.getDescriptor()}"
                    classpath.append(lib)
                self.monitor.message(f"    {lib.absolute()}")

            if err:
                self.error(f"  Missing Processor Dependencies: {err}")
                return

            args = []
            for arg in proc.getArgs():
                if arg.startswith("[") and arg.endswith("]"):  # Library
                    artifact = Artifact.from_(arg[1:-1])
                    args.append(artifact.getLocalPath(librariesDir).absolute())
                else:
                    args.append(Util.replaceTokens(data, arg))
            if err:
                self.error(f"  Missing Processor data values: {err}")
                return None
            """
             monitor.message("  Args: " + args.stream().map(a -> a.indexOf(' ') != -1 || a.indexOf(',') != -1 ? '"' + a + '"' : a).collect(Collectors.joining(", ")));
            """
            self.monitor.message("  Args: " + str([
                a if a.indexOf(' ') != -1 or a.indexOf(',') != -1 else f'"{a}"' for a in args
            ]))
            # TODO: continue translate PostProcessors.java:210

    def __loadData(self, librariesDir: Path) -> Optional[Dict[str, __DataEntry]]:
        """
        :raise IOError
        """

        cfg = self.profile.getData(self.isClient)
        if len(cfg) == 0:
            return {}

        rv = {}
        err = ""

        # Path temp  = Files.createTempDirectory("forge_installer");
        temp = Path(tempfile.mkdtemp("forge_installer"))
        self.monitor.start(f"Created Temporary Directory: {temp}")

        steps = len(cfg)
        progress = 1

        for key, value in cfg.items():
            self.monitor.progress(progress / steps)
            progress += 1

            if value.startswith("[") and value.endswith("]"):  # Artifact
                artifact = Artifact.from_(value[1:-1])
                entry = PostProcessors.__ArtifactEntry(artifact, librariesDir)
            elif value.startswith("'") and value.endswith("'"):  # Literal
                entry = PostProcessors.__DataEntry(value[1:-1])
            else:
                target = temp / value
                self.monitor.message(f"Extracting {value} to {target}")
                if not DownloadUtils.extractFile(value, target):
                    err += "\n  "
                    err += value
                entry = PostProcessors.__FileEntry(target)

            rv[key] = entry

        if err:
            self.error(f"Failed to extract files from archive: {err}")
            return None

        return rv

    def buildOutputs(self, librariesDir, data):
        rv: List[List[PostProcessors.__Output]] = []

        for proc in self.processors:
            outputs = proc.getOutputs()
            if len(outputs) == 0:
                rv.append([])
                continue

            pout: List[PostProcessors.__Output] = []
            for key in outputs.keys():

                file: str
                if key.startswith("[") and key.endswith("]"):  # Artifact
                    file = str(Artifact.from_(key[1:-1]).getLocalPath(librariesDir).absolute())
                else:
                    file = Util.replaceTokens(data, key)

                value = outputs.get(key)
                if value is not None:
                    value = Util.replaceTokens(data, value)

                if (key is None or value is None):
                    self.error(f"  Invalid configuration, bad output config: [{key}: {value}]")
                    return None

                pout.append(PostProcessors.__Output(Path(file), value))

            rv.append(pout)

        return rv

    def log(self, msg: str):
        ...
