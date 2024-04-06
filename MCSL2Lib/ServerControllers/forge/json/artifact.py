"""
/*
 * Copyright (c) Forge Development LLC
 * SPDX-License-Identifier: LGPL-2.1-only
 */
package net.minecraftforge.installer.json;

import java.io.File;
import java.lang.reflect.Type;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonNull;
import com.google.gson.JsonParseException;
import com.google.gson.JsonPrimitive;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

public class Artifact {
    //Descriptor parts: group:name:version[:classifier][@extension]
    private String domain;
    private String name;
    private String version;
    private String classifier = null;
    private String ext = "jar";

    //Caches so we don't rebuild every time we're asked.
    private String path;
    private String file;
    private String descriptor;

    public static Artifact from(String descriptor)
    {
        Artifact ret = new Artifact();
        ret.descriptor = descriptor;

        String[] pts = descriptor.split(":");
        ret.domain = pts[0];
        ret.name = pts[1];

        int last = pts.length - 1;
        int idx = pts[last].indexOf('@');
        if (idx != -1) {
            ret.ext = pts[last].substring(idx + 1);
            pts[last] = pts[last].substring(0, idx);
        }

        ret.version = pts[2];
        if (pts.length > 3)
            ret.classifier = pts[3];

        ret.file = ret.name + '-' + ret.version;
        if (ret.classifier != null) ret.file += '-' + ret.classifier;
        ret.file += '.' + ret.ext;

        ret.path = ret.domain.replace('.', '/') + '/' + ret.name + '/' + ret.version + '/' + ret.file;

        return ret;
    }

    public File getLocalPath(File base) {
        return new File(base, path.replace('/', File.separatorChar));
    }

    public String getDescriptor(){ return descriptor; }
    public String getPath()      { return path;       }
    public String getDomain()    { return domain;     }
    public String getName()      { return name;       }
    public String getVersion()   { return version;    }
    public String getClassifier(){ return classifier; }
    public String getExt()       { return ext;        }
    public String getFilename()  { return file;       }
    @Override
    public String toString() {
        return getDescriptor();
    }

    public static class Adapter implements JsonDeserializer<Artifact>, JsonSerializer<Artifact> {
        @Override
        public JsonElement serialize(Artifact src, Type typeOfSrc, JsonSerializationContext context) {
            return src == null ? JsonNull.INSTANCE : new JsonPrimitive(src.getDescriptor());
        }

        @Override
        public Artifact deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
            return json.isJsonPrimitive() ? Artifact.from(json.getAsJsonPrimitive().getAsString()) : null;
        }
    }
}

"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Artifact:
    domain: str
    name: str
    version: str
    classifier: str = None
    ext: str = "jar"

    # Caches so we don't rebuild every time we're asked.
    path: str = None
    file: str = None
    descriptor: str = None

    def from_(self, descriptor: str) -> 'Artifact':
        pts = descriptor.split(":")
        domain = pts[0]
        name = pts[1]

        last = len(pts) - 1
        idx = pts[last].find("@")

        if idx != -1:
            ext = pts[last][idx + 1:]
            pts[last] = pts[last][:idx]
        else:
            ext = "jar"

        version = pts[2]
        classifier = pts[3] if len(pts) > 3 else None

        file = name + "-" + version
        if classifier is not None:
            file += "-" + classifier
        file += "." + ext

        path = domain.replace(".", "/") + "/" + name + "/" + version + "/" + file

        return Artifact(
            domain=domain,
            name=name,
            version=version,
            classifier=classifier,
            ext=ext,
            path=path,
            file=file,
            descriptor=descriptor,
        )
    
    def getLocalPath(self, base: Path) -> Path:
        return base / self.path.replace("/", Path.sep)
    
    def getDescriptor(self) -> str:
        return self.descriptor
    
    def getPath(self) -> str:
        return self.path
    
    def getDomain(self) -> str:
        return self.domain
    
    def getName(self) -> str:
        return self.name
    
    def getVersion(self) -> str:
        return self.version
    
    def getClassifier(self) -> str:
        return self.classifier
    
    def getExt(self) -> str:
        return self.ext
    
    def getFilename(self) -> str:
        return self.file
    
    def __str__(self) -> str:
        return self.descriptor
    
    # TODO: custom json adapter
