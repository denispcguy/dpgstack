# ZSH
Shell setup for Unix-based workstations.

## Workflow: Install Oh My Zsh with autosuggestions
1. Install ZSH if not already present:
    ```
    apt install zsh
    ```
2. Install Oh My Zsh:
    ```
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```
3. Install the autosuggestions plugin:
    ```
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    ```
4. Enable the plugin by editing `~/.zshrc` — add `zsh-autosuggestions` to the `plugins` list:
    ```
    plugins=(git zsh-autosuggestions)
    ```

See `shell_setup/.zshrc` in the generated project for the recommended Dpgstack ZSH configuration.