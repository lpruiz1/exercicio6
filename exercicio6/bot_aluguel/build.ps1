$exclude = @("venv", "bot_aluguel.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot_aluguel.zip" -Force