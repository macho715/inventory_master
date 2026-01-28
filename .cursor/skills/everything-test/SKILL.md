---
name: everything-test
description: Test Everything integration (ES CLI, HTTP Server, SDK). Use to verify Everything connectivity and provider availability.
---

# Everything Test

## When to Use
- Everything 연동 상태를 확인할 때
- Provider 가용성을 테스트할 때
- Everything 설정 문제를 진단할 때

## Instructions

### ES CLI Test
```powershell
# 1. Everything 실행 확인
Get-Process Everything -ErrorAction SilentlyContinue

# 2. ES CLI 테스트
es.exe test

# 3. 간단한 검색 테스트
es.exe "*.pdf" | Select-Object -First 5
```

### HTTP Server Test
```powershell
# 1. HTTP Server 상태 확인
curl http://localhost:8080/

# 2. 검색 API 테스트
curl "http://localhost:8080/?s=*.pdf&count=5"

# 3. 인증 테스트 (설정된 경우)
curl -u username:password "http://localhost:8080/"
```

### SDK Test (Python)
```python
# SDK 연결 테스트
from inventory_master.providers.everything_es import EverythingESCLI

provider = EverythingESCLI()
results = provider.search("*.pdf", max_results=5)
print(f"Found {len(results)} files")
```

## Output
- Provider availability status
- Connection test results
- Fallback recommendation (if Everything unavailable)
- Configuration issues (if any)

## Troubleshooting
- Everything 미실행 → 로컬 스캐너 fallback 안내
- HTTP Server 미활성화 → ES CLI 사용 권장
- 인증 실패 → 인증 설정 확인 안내
