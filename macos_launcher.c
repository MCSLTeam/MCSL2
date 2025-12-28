#include <unistd.h>
#include <libgen.h>
#include <limits.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    char exePath[PATH_MAX];
    realpath(argv[0], exePath);
    char *exeDir = dirname(exePath);

    chdir(exeDir);

    setenv("PATH", "/usr/bin:/bin:/usr/sbin:/sbin", 1);
    setenv(
        "PYTHONHOME",
        "../Resources/Python/Versions/3.8",
        1
    );
    setenv(
        "PYTHONPATH",
        "../Resources/Python/Versions/3.8/lib/python3.8/site-packages",
        1
    );
    setenv(
        "QT_PLUGIN_PATH",
        "../Resources/Python/Versions/3.8/lib/python3.8/site-packages/PyQt5/Qt/plugins",
        1
    );

    execl(
        "../Resources/Python/Versions/3.8/bin/python3",
        "python3",
        "../MacOS/MCSL2Contents/MCSL2.py",
        NULL
    );

    perror("execl failed");
    return 1;
}
