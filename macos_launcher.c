#include <unistd.h>
#include <libgen.h>
#include <limits.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    char exePath[PATH_MAX];
    if (realpath(argv[0], exePath) == NULL) {
        return 1;
    }
    char *exeDir = dirname(exePath);
    chdir(exeDir);
    setenv("PATH", "/usr/bin:/bin:/usr/sbin:/sbin", 1);
    setenv(
        "PYTHONPATH",
        "Python3.framework/Versions/3.8/lib/python3.8/site-packages",
        1
    );

    setenv(
        "QT_PLUGIN_PATH",
        "Python3.framework/Versions/3.8/lib/python3.8/site-packages/PyQt5/Qt/plugins",
        1
    );
    execl(
        "Python3.framework/Versions/3.8/bin/python3",
        "python3",
        "MCSL2Contents/MCSL2.py",
        NULL
    );
    perror("execl failed");
    return 1;
}
