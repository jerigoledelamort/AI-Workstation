# VRAM/RAM Monitor
nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu --format=csv,noheader
Write-Host ""
$os = Get-CimInstance Win32_OperatingSystem
$totalRAM = [math]::Round($os.TotalVisibleMemorySize/1MB, 1)
$freeRAM = [math]::Round($os.FreePhysicalMemory/1MB, 1)
$usedRAM = $totalRAM - $freeRAM
Write-Host "RAM: ${usedRAM}GB / ${totalRAM}GB (Free: ${freeRAM}GB)"