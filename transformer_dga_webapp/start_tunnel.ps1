# Persistent SSH Tunnel for Remote/Mobile Access
while ($true) {
    Write-Host "Connecting to localhost.run tunnel..."
    ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=15 -o ServerAliveCountMax=6 -R 80:localhost:8501 nokey@localhost.run
    Write-Host "Tunnel disconnected. Reconnecting in 3 seconds..."
    Start-Sleep -Seconds 3
}
