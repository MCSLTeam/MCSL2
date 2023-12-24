Write-Host "    __  ______________                           __                           __                 ___
   /  |/  / ____/ ___/___  ______   _____  _____/ /   ____ ___  ______  _____/ /_  ___  _____   |__ \
  / /|_/ / /    \__ \/ _ \/ ___/ | / / _ \/ ___/ /   / __ `/ / / / __ \/ ___/ __ \/ _ \/ ___/   __/ /
 / /  / / /___ ___/ /  __/ /   | |/ /  __/ /  / /___/ /_/ / /_/ / / / / /__/ / / /  __/ /      / __/
/_/  /_/\____//____/\___/_/    |___/\___/_/  /_____/\__,_/\__,_/_/ /_/\___/_/ /_/\___/_/      /____/
-----------------------------------------------------------------------------------------------------
Installation Script"

###################################
# Select Python
###################################
$existPythonList = Get-Command python -All | Select-Object -ExpandProperty Source
$selectedPython = $null
while ($selectedPython -eq $null) {
    Write-Host "Choose Python version, required version: >=3.8,<3.9 :"
    $i = 1
    $existPythonList | ForEach-Object {
        Write-Host "$i. $_"
        $i++
    }

    $choice = Read-Host -Prompt "Enter the number of the desired Python version"
    if ($choice -ge 1 -and $choice -le $existPythonList.Count) {
        $selectedPython = $existPythonList[$choice - 1]
    } else {
        Write-Host "Invalid selection. Please enter a valid number."
    }
}

###################################
# Check PDM
###################################
Write-Host "Start to check package manager..."
$pdmInstall = Read-Host -Prompt "Have you installed pdm? We need this to install dependencies. (y/n)"

if ($pdmInstall -eq "n") {

    $pipxUsage = Read-Host -Prompt "Do you want to use pipx to install pdm (Recommended)? (y/n)"

    if ($pipxUsage -eq "y") {

        $pipxInstall = Read-Host -Prompt "Have you installed pipx? If no, we will help you do this. (y/n)"

        if ($pipxInstall -eq "n") {
            Write-Host "Installing pipx..."
            & $selectedPython -m pip install --user pipx
            & $selectedPython -m pipx ensurepath
        }
        & $selectedPython -m pipx install pdm
        Write-Host "pdm has been installed successfully with pipx."
    } else {
        & $selectedPython -m pip install --user pdm
        Write-Host "pdm has been installed successfully with pip."
    }
}
###################################
# Venv
###################################
Write-Host "Start to create environment..."
$useVenv = Read-Host -Prompt "Do you want a virtual environment? (y/n)"
if ($useVenv -eq "n") {
    & pdm use $selectedPython
} else {
    & pdm venv create $selectedPython
    & pdm use --venv in-project
}
###################################
# Install dependencies
###################################
Write-Host "Start to install dependencies..."
$isDev = Read-Host -Prompt "Do you want to install dev dependencies? (y/n)"
if ($isDev -eq "n") {
    & pdm install --no-self --fail-fast
} else {
    & pdm install --no-self --fail-fast --dev
}
Write-Host "Success. Start your MCServerLauncher 2 now!"
exit