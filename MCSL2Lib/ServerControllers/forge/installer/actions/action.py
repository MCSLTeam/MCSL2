from .post_processors import PostProcessors
from .progress_callback import ProgressCallback
from ..json.installV1 import InstallV1
from ..json.util import Util
from ..json.version import Version

"""
/*
 * Copyright (c) Forge Development LLC
 * SPDX-License-Identifier: LGPL-2.1-only
 */
package net.minecraftforge.installer.actions;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import javax.swing.JOptionPane;

import net.minecraftforge.installer.DownloadUtils;
import net.minecraftforge.installer.SimpleInstaller;
import net.minecraftforge.installer.json.Artifact;
import net.minecraftforge.installer.json.InstallV1;
import net.minecraftforge.installer.json.Util;
import net.minecraftforge.installer.json.Version;
import net.minecraftforge.installer.json.Version.Download;
import net.minecraftforge.installer.json.Version.Library;
import net.minecraftforge.installer.json.Version.LibraryDownload;

public abstract class Action {
    protected final InstallV1 profile;
    protected final ProgressCallback monitor;
    protected final PostProcessors processors;
    protected final Version version;
    private List<Artifact> grabbed = new ArrayList<>();

    protected Action(InstallV1 profile, ProgressCallback monitor, boolean isClient) {
        this.profile = profile;
        this.monitor = monitor;
        this.processors = new PostProcessors(profile, isClient, monitor);
        this.version = Util.loadVersion(profile);
    }

    protected void error(String message) {
        if (!SimpleInstaller.headless)
            JOptionPane.showMessageDialog(null, message, "Error", JOptionPane.ERROR_MESSAGE);
        monitor.stage(message);
    }

    public abstract boolean run(File target, File installer) throws ActionCanceledException;
    public abstract boolean isPathValid(File targetDir);
    public abstract String getFileError(File targetDir);
    public abstract String getSuccessMessage();

    protected List<Library> getLibraries() {
        List<Library> libraries = new ArrayList<>();
        libraries.addAll(Arrays.asList(version.getLibraries()));
        libraries.addAll(Arrays.asList(processors.getLibraries()));
        return libraries;
    }

    protected boolean downloadLibraries(File librariesDir, List<File> additionalLibDirs) throws ActionCanceledException {
        monitor.start("Downloading libraries");
        monitor.message(String.format("Found %d additional library directories", additionalLibDirs.size()));

        List<Library> libraries = getLibraries();

        StringBuilder output = new StringBuilder();
        final double steps = libraries.size();
        int progress = 1;

        for (Library lib : libraries) {
            checkCancel();
            monitor.progress(progress++ / steps);
            if (!DownloadUtils.downloadLibrary(monitor, profile.getMirror(), lib, librariesDir, grabbed, additionalLibDirs)) {
                LibraryDownload download = lib.getDownloads() == null ? null :  lib.getDownloads().getArtifact();
                if (download != null && !download.getUrl().isEmpty()) // If it doesn't have a URL we can't download it, assume we install it later
                    output.append('\n').append(lib.getName());
            }
        }
        String bad = output.toString();
        if (!bad.isEmpty()) {
            error("These libraries failed to download. Try again.\n" + bad);
            return false;
        }
        return true;
    }

    protected int downloadedCount() {
        return grabbed.size();
    }

    protected int getTaskCount() {
        return profile.getLibraries().length + processors.getTaskCount();
    }

    protected void checkCancel() throws ActionCanceledException {
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            throw new ActionCanceledException(e);
        }
    }

    protected boolean downloadVanilla(File target, String side) {
        if (!target.exists()) {
            File parent = target.getParentFile();
            if (!parent.exists())
                parent.mkdirs();

            String resource = "/cache/vanilla/" + side + ".jar";
            try (final InputStream input = Action.class.getResourceAsStream(resource)) {
                if (input != null) {
                    monitor.message("  Extracting from " + resource);
                    Files.copy(input, target.toPath(), StandardCopyOption.REPLACE_EXISTING);
                    return true;
                }
            } catch (IOException e) {
                error("Failed to extract vanilla jar from " + resource);
                e.printStackTrace();
                return false;
            }

            Version vanilla = Util.getVanillaVersion(profile.getMinecraft());
            if (vanilla == null) {
                error("Failed to download version manifest, can not find " + side + " jar URL.");
                return false;
            }

            Download dl = vanilla.getDownload(side);
            if (dl == null) {
                error("Failed to download minecraft " + side + " jar, info missing from manifest");
                return false;
            }

            if (!DownloadUtils.download(monitor, profile.getMirror(), dl, target)) {
                target.delete();
                error("Downloading minecraft " + side + " failed, invalid checksum.\n" + (
                    "client".equals(side) ?
                        "Try again, or use the vanilla launcher to install the vanilla version." :
                        "Try again, or manually place server jar to skip download."
                    ));
                return false;
            }
        }

        return true;
    }
}
"""


class Action:
    profile: InstallV1
    monitor: ProgressCallback
    processors: PostProcessors
    version: Version

    def __init__(self, profile: InstallV1, monitor: ProgressCallback, isClient: bool):
        self.profile = profile
        self.monitor = monitor
        self.processors = PostProcessors(profile, isClient, monitor)
        self.version = Util.loadVersion(profile)

    def checkCancel(self):
        ...


class ActionCanceledException(Exception):
    def __init__(self):
        super().__init__()
