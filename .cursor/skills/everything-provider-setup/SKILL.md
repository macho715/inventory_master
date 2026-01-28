---
name: everything-provider-setup
description: Set up Everything for read-only inventory via ES CLI or HTTP server. Use when integrating Everything, configuring search providers, or setting up fast file indexing. Supports ES CLI (recommended), HTTP Server, and SDK with automatic fallback.
---

# Everything Provider Setup (Read-only)

## When to Use
- Initial Everything integration setup
- Configuring Everything ES CLI (`es.exe`)
- Enabling HTTP server for search-only use
- Setting up SDK integration
- Troubleshooting Everything connectivity
- Before running `inventory-report` skill

## Prerequisites
- Everything installed: https://www.voidtools.com/
- Everything running in background (system tray)
- Administrator privileges (for ES CLI installation)
- Python environment (for SDK integration)

## Provider Priority

### Recommended Order
1. **ES CLI** (most stable, batch-friendly)
2. **HTTP Server** (web API, requires security config)
3. **SDK** (direct DLL, advanced use)
4. **Fallback** (local file system scan, always available)

## Method 1: ES CLI (Recommended)

### Installation
1. Download `es.exe` from Everything website
2. Add to system PATH or project directory
3. Verify Everything is running:
   ```powershell
   Get-Process Everything -ErrorAction SilentlyContinue
   ```

### Configuration
```powershell
# Test ES CLI connection
es.exe test

# Expected output: Connection successful
```

### Validation
```powershell
# Simple search test
es.exe "*.pdf" | Select-Object -First 5

# Export to CSV (if needed)
es.exe -export-csv results.csv "*.pdf"

# With metadata
es.exe -size -date-modified "*.pdf"
```

### Integration
- Works with `inventory-report` skill
- Used by `LocalWalkProvider` as fallback
- Fast batch operations
- No network exposure risk

## Method 2: HTTP Server (Riskier)

### Security Requirements
⚠️ **Critical**: Must follow security checklist

### Configuration Steps
1. Open Everything: Tools → Options → HTTP Server
2. **Enable HTTP Server** (check box)
3. **Bind to 127.0.0.1 only** (not 0.0.0.0)
4. **Set username/password** (required)
5. **Disable "Allow file download"** (critical)
6. **Set port** (default: 8080, use non-standard if possible)
7. Save settings

### Security Checklist
- [ ] Bound to 127.0.0.1 (loopback only)
- [ ] Username/password set
- [ ] "Allow file download" disabled
- [ ] Non-standard port (if possible)
- [ ] Firewall rules configured (block external access)
- [ ] HTTPS enabled (if available)

### Validation
```powershell
# Test HTTP server (local only)
curl http://127.0.0.1:8080/

# Search API test
curl "http://127.0.0.1:8080/?s=*.pdf&count=5"

# With authentication
curl -u username:password "http://127.0.0.1:8080/"
```

### Risks
- **External exposure**: If bound to 0.0.0.0
- **File download**: If enabled, allows file access
- **No authentication**: Default has no auth
- **Network scanning**: Exposed endpoints discoverable

## Method 3: SDK (Advanced)

### Requirements
- Everything SDK DLL (`Everything32.dll` or `Everything64.dll`)
- Python `ctypes` library
- Matching architecture (32-bit or 64-bit)

### Setup
```python
from ctypes import windll, create_unicode_buffer

# Load DLL
dll = windll.LoadLibrary("Everything64.dll")

# Test connection
version = dll.Everything_GetVersion()
print(f"Everything version: {version}")
```

### Integration
- Direct DLL access
- Fastest performance
- Requires architecture matching
- More complex setup

## Automatic Fallback

### Provider Selection
The system automatically tries providers in order:
1. ES CLI → 2. HTTP Server → 3. SDK → 4. Local Scan

### Fallback Behavior
- If Everything unavailable → uses `LocalWalkProvider`
- Local scan is slower but always works
- No error thrown, graceful degradation

## Integration Points

### Works With
- **`inventory-report` skill**: Uses Everything for fast scanning
- **`everything-test` skill**: Validates provider setup
- **`planner` agent**: Uses Everything for file discovery
- **`LocalWalkProvider`**: Fallback when Everything unavailable

### Typical Workflow
```
everything-provider-setup
  → everything-test (validate)
  → inventory-report (use Everything)
  → planner (file discovery)
```

## Configuration Output

### Checklist Format
```
Everything Provider Setup Checklist:
- [x] Everything installed
- [x] Everything running
- [x] ES CLI on PATH
- [x] ES CLI test passed
- [ ] HTTP Server configured (optional)
- [ ] SDK configured (optional)
```

### Proof Commands
```powershell
# ES CLI validation
es.exe test
# Expected: Connection successful

# HTTP Server validation (if enabled)
curl http://127.0.0.1:8080/
# Expected: HTTP 200 OK

# Provider priority
1. ES CLI: Available ✓
2. HTTP Server: Not configured
3. SDK: Not configured
4. Fallback: Always available ✓
```

## Troubleshooting

### ES CLI Not Found
- **Issue**: `es.exe` not on PATH
- **Solution**: Add to PATH or use full path
- **Verify**: `where.exe es.exe`

### Everything Not Running
- **Issue**: Everything process not found
- **Solution**: Start Everything from Start Menu
- **Verify**: `Get-Process Everything`

### HTTP Server Connection Failed
- **Issue**: Cannot connect to HTTP server
- **Check**: Everything → Tools → Options → HTTP Server enabled
- **Check**: Bound to 127.0.0.1 (not 0.0.0.0)
- **Check**: Firewall blocking localhost

### SDK Load Failed
- **Issue**: DLL not found or architecture mismatch
- **Solution**: Ensure correct DLL (32/64-bit) matches Python
- **Verify**: `python -c "import platform; print(platform.architecture())"`

### Fallback to Local Scan
- **Normal behavior**: If Everything unavailable
- **Performance**: Slower but functional
- **No action needed**: System handles automatically

## Security Best Practices

### ES CLI
- ✅ Safe: Local process communication only
- ✅ No network exposure
- ✅ Recommended for most use cases

### HTTP Server
- ⚠️ **Must bind to 127.0.0.1 only**
- ⚠️ **Must set username/password**
- ⚠️ **Must disable file download**
- ⚠️ **Use firewall to block external access**

### SDK
- ✅ Safe: Direct DLL access
- ✅ No network exposure
- ⚠️ Requires matching architecture

## Additional Resources
- For testing: `everything-test` skill
- For usage: `inventory-report` skill
- For detailed guide: `docs/everything_integration.md`
- For provider code: `src/inventory_master/providers/`
