from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Iterable, Mapping

from .artifact import Artifact
from .base_model import BaseModel
from .mirror import Mirror
from .spec import Spec
from .version import Version
from ..download_utils import DownloadUtils

"""
public class Install extends Spec {
    // Profile name to install and direct at this new version
    protected String profile;
    // Version name to install to.
    protected String version;
    // Icon to display in the list
    protected String icon;
    // Vanilla version this is based off of.
    protected String minecraft;
    // Version json to install into the client
    protected String json;
    // Logo to be displayed on the installer GUI.
    protected String logo;
    // Maven artifact path for the 'main' jar to install.
    protected Artifact path;
    // Icon to use for the url button
    protected String urlIcon;
    // Welcome message displayed on main install panel.
    protected String welcome;
    // URL for mirror list, which needs to be a json file in the format of an array of Mirror
    protected String mirrorList;
    //Hides an entry from the install UI
    protected boolean hideClient, hideServer, hideExtract, hideOffline = false;
    // Extra libraries needed by processors, that may differ from the installer version's library list. Uses the same format as Mojang for simplicities sake.
    protected Version.Library[] libraries;
    // Executable jars to be run after all libraries have been downloaded.
    protected List<Processor> processors;
    //Data files to be extracted during install, used for processor.
    protected Map<String, DataFile> data;

    // non-serialized values
    private Mirror mirror;
    private boolean triedMirrors = false;

    public String getProfile() {
        return profile;
    }

    public String getVersion() {
        return version;
    }

    public String getIcon() {
        return this.icon;
    }

    public String getMinecraft() {
        return minecraft;
    }

    public String getJson() {
        return json;
    }

    public String getLogo() {
        return logo;
    }

    public Artifact getPath() {
        return path;
    }

    public String getUrlIcon() {
        return urlIcon == null ? "/url.png" : urlIcon;
    }

    public String getWelcome() {
        return welcome == null ? "" : welcome;
    }

    public String getMirrorList() {
        return mirrorList;
    }

    public Mirror getMirror() {
        if (mirror != null)
            return mirror;
        if (SimpleInstaller.mirror != null) {
            mirror = new Mirror("Mirror", "", "", SimpleInstaller.mirror.toString());
            return mirror;
        }
        if (getMirrorList() == null)
            return null;
        if (!triedMirrors) {
            triedMirrors = true;
            Mirror[] list = DownloadUtils.downloadMirrors(getMirrorList());
            mirror = list == null || list.length == 0 ? null : list[new Random().nextInt(list.length)];
        }
        return mirror;
    }

    public boolean hideClient() {
        return hideClient;
    }

    public boolean hideServer() {
        return hideServer;
    }

    public boolean hideExtract() {
        return hideExtract;
    }

    public boolean hideOffline() {
        return hideOffline;
    }

    public Version.Library[] getLibraries() {
        return libraries == null ? new Version.Library[0] : libraries;
    }

    public List<Processor> getProcessors(String side) {
        if (processors == null) return Collections.emptyList();
        return processors.stream().filter(p -> p.isSide(side)).collect(Collectors.toList());
    }

    public Map<String, String> getData(boolean client) {
        if (data == null)
            return new HashMap<>();

        return data.entrySet().stream().collect(Collectors.toMap(Entry::getKey, e -> client ? e.getValue().client : e.getValue().server));
    }

    public static class Processor {
        // Which side this task is to be run on, Currently know sides are "client", "server" and "extract", if this omitted, assume all sides.
        private List<String> sides;
        // The executable jar to run, The installer will run it in-process, but external tools can run it using java -jar {file}, so MANIFEST Main-Class entry must be valid.
        private Artifact jar;
        // Dependency list of files needed for this jar to run. Anything listed here SHOULD be listed in {@see Install#libraries} so the installer knows to download it.
        private Artifact[] classpath;
        /*
         * Arguments to pass to the jar, can be in the following formats:
         * [Artifact] : A artifact path in the target maven style repo, where all libraries are downloaded to.
         * {DATA_ENTRY} : A entry in the Install#data map, extract as a file, there are a few extra specified values to allow the same processor to run on both sides:
         *   {MINECRAFT_JAR} - The vanilla minecraft jar we are dealing with, /versions/VERSION/VERSION.jar on the client and /minecraft_server.VERSION.jar for the server
         *   {SIDE} - Either the exact string "client", "server", and "extract" depending on what side we are installing.
         */
        private String[] args;
        /*
         *  Files output from this task, used for verifying the process was successful, or if the task needs to be rerun.
         *  Keys are either a [Artifact] or {DATA_ENTRY}, if it is a {DATA_ENTRY} then that MUST be a [Artifact]
         *  Values are either a {DATA_ENTRY} or 'value', if it is a {DATA_ENTRY} then that entry MUST be a quoted string literal
         *    The end string literal is the sha1 hash of the specified artifact.
         */
        private Map<String, String> outputs;

        public boolean isSide(String side) {
            return sides == null || sides.contains(side);
        }

        public Artifact getJar() {
            return jar;
        }

        public Artifact[] getClasspath() {
            return classpath == null ? new Artifact[0] : classpath;
        }

        public String[] getArgs() {
            return args == null ? new String[0] : args;
        }

        public Map<String, String> getOutputs() {
            return outputs == null ? Collections.emptyMap() : outputs;
        }
    }

    public static class DataFile {
        /**
         * Can be in the following formats:
         * [value] - An absolute path to an artifact located in the target maven style repo.
         * 'value' - A string literal, remove the 's and use this value
         * value - A file in the installer package, to be extracted to a temp folder, and then have the absolute path in replacements.
         */
        // Value to use for the client install
        private String client;
        // Value to use for the server install
        private String server;

        public String getClient() {
            return client;
        }
        public String getServer() {
            return server;
        }
    }
}
"""


@dataclass
class Install(Spec):
    profile: str
    version: str
    icon: str
    minecraft: str
    json: str
    logo: str
    path: Artifact
    urlIcon: str
    welcome: str
    mirrorList: str

    libraries: List[Version.Library]
    processors: List['Install.Processor']  # type: List[Install.Processor]
    data: Dict[str, 'Install.DataFile']  # type: Dict[str, Install.DataFile]

    # non-serializable
    mirror: Mirror
    triedMirrors: bool = False

    hideClient: bool = False
    hideServer: bool = False
    hideExtract: bool = False
    hideOffline: bool = False

    def getProfile(self) -> str:
        return self.profile

    def getVersion(self) -> str:
        return self.version

    def getIcon(self) -> str:
        return self.icon

    def getMinecraft(self) -> str:
        return self.minecraft

    def getJson(self) -> str:
        return self.json

    def getLogo(self) -> str:
        return self.logo

    def getPath(self) -> Artifact:
        return self.path

    def getUrlIcon(self) -> str:
        return "/url.png" if self.urlIcon is None else self.urlIcon

    def getWelcome(self) -> str:
        return "" if self.welcome is None else self.welcome

    def getMirrorList(self) -> str:
        return self.mirrorList

    def getMirror(self) -> Optional[Mirror]:
        from ..simple_installer import SimpleInstaller

        custom_mirror = SimpleInstaller.mirror

        if (self.mirror is not None):
            return self.mirror
        if (custom_mirror != None):
            self.mirror = Mirror("Mirror", "", "", custom_mirror if custom_mirror is None else "")
            return self.mirror
        if self.getMirrorList() is None:
            return None
        if (not self.triedMirrors):
            self.triedMirrors = True
            list_: List[Mirror] = DownloadUtils.downloadMirrors(self.getMirrorList())
            self.mirror = None if not list_ else list_[random.randint(0, len(list_) - 1)]
        return self.mirror

    def getLibraries(self) -> List[Version.Library]:
        return [] if self.libraries is None else self.libraries

    def getProcessors(self, side: str) -> List['Install.Processor']:
        if self.processors is None:
            return []
        return [p for p in self.processors if p.isSide(side)]

    def getData(self, client: bool) -> Dict[str, str]:
        if self.data is None:
            return {}
        return {k: (v.client if client else v.server) for k, v in self.data.items()}

    @classmethod
    def libraries_factory(cls, items: Iterable):
        rv = []
        for i in items:
            rv.append(Version.Library.of(i))
        return rv

    @classmethod
    def processors_factory(cls, items: Iterable):
        return [Install.Processor.of(i) for i in items]

    @classmethod
    def data_factory(cls, items: Mapping[str, Mapping]):
        return {k: Install.DataFile(**v) for k, v in items.items()}

    @dataclass
    class Processor(BaseModel):
        sides: List[str] = None
        jar: Artifact = None
        classpath: List[Artifact] = None
        args: List[str] = None
        outputs: Dict[str, str] = None

        def isSide(self, side: str) -> bool:
            return self.sides is None or side in self.sides

        def getJar(self) -> Artifact:
            return self.jar

        def getClasspath(self) -> List[Artifact]:
            return [] if self.classpath is None else self.classpath

        def getArgs(self) -> List[str]:
            return [] if self.args is None else self.args

        def getOutputs(self) -> Dict[str, str]:
            return {} if self.outputs is None else self.outputs

        @classmethod
        def jar_factory(cls, item):
            return Artifact.from_(json.dumps(item))

        @classmethod
        def classpath_factory(cls, items: Iterable):
            return [Artifact.from_(json.dumps(i)) for i in items]

    @dataclass
    class DataFile:
        # /**
        #  * Can be in the following formats:
        #  * [value] - An absolute path to an artifact located in the target maven style repo.
        #  * 'value' - A string literal, remove the 's and use this value
        #  * value - A file in the installer package, to be extracted to a temp folder, and then have the absolute path in replacements.
        #  */

        client: str = None
        server: str = None

        def getClient(self) -> str:
            return self.client

        def getServer(self) -> str:
            return self.server
