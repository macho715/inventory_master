# Everything 연동 가이드

## 개요

Everything은 Windows용 초고속 파일 검색 도구입니다. 이 프로젝트에서는 **Read-only 조회 전용**으로 사용하며, 세 가지 연동 방법을 제공합니다.

## 사전 준비

1. **Everything 설치**
   - 다운로드: https://www.voidtools.com/
   - 기본 설치 경로: `C:\Program Files\Everything\Everything.exe`

2. **Everything 실행 확인**
   - Everything이 백그라운드에서 실행 중이어야 합니다.
   - 시스템 트레이 아이콘으로 확인 가능

3. **설정 확인**
   - Tools → Options → HTTP Server (필요시 활성화)
   - Tools → Options → ETP/FTP Server (필요시 활성화)

---

## 방법 1: ES CLI (권장 1순위)

### 특징
- **가장 안정적이고 배치 작업에 적합**
- 명령줄 인터페이스로 스크립트 통합 용이
- CSV/JSON 출력 지원

### 기본 사용법

```bash
# 기본 검색
es.exe "*.pdf"

# 특정 폴더 검색
es.exe "C:\Users\*.pdf"

# 결과를 CSV로 저장
es.exe -export-csv results.csv "*.pdf"

# 결과를 JSON으로 저장 (JSON 출력 지원 시)
es.exe -export-json results.json "*.pdf"

# 파일 크기, 수정일 등 메타데이터 포함
es.exe -size -date-modified "*.pdf"
```

### Python 연동 예시

```python
import subprocess
import json
import csv
from pathlib import Path
from typing import List, Dict, Optional

class EverythingESCLI:
    """Everything ES CLI Provider"""
    
    def __init__(self, es_path: Optional[str] = None):
        """
        Args:
            es_path: Everything ES CLI 경로 (기본값: 자동 탐색)
        """
        self.es_path = es_path or self._find_es_path()
        if not self.es_path or not Path(self.es_path).exists():
            raise FileNotFoundError("Everything ES CLI를 찾을 수 없습니다.")
    
    def _find_es_path(self) -> Optional[str]:
        """Everything ES CLI 경로 자동 탐색"""
        common_paths = [
            r"C:\Program Files\Everything\es.exe",
            r"C:\Program Files (x86)\Everything\es.exe",
            r"C:\Tools\Everything\es.exe",
        ]
        for path in common_paths:
            if Path(path).exists():
                return path
        return None
    
    def search(
        self,
        query: str,
        max_results: int = 10000,
        export_csv: Optional[str] = None,
        include_metadata: bool = True
    ) -> List[Dict[str, str]]:
        """
        Everything 검색 실행
        
        Args:
            query: 검색 쿼리 (예: "*.pdf", "C:\\Users\\*.txt")
            max_results: 최대 결과 수
            export_csv: CSV 파일로 저장할 경로 (선택)
            include_metadata: 크기, 수정일 등 메타데이터 포함 여부
        
        Returns:
            검색 결과 리스트 (경로, 크기, 수정일 등)
        """
        cmd = [self.es_path, query]
        
        if include_metadata:
            cmd.extend(["-size", "-date-modified", "-date-created"])
        
        if export_csv:
            cmd.extend(["-export-csv", export_csv])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                encoding="utf-8"
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"ES CLI 실행 실패: {result.stderr}")
            
            # CSV 파일이 생성된 경우 파싱
            if export_csv and Path(export_csv).exists():
                return self._parse_csv(export_csv)
            
            # 표준 출력 파싱
            return self._parse_stdout(result.stdout)
            
        except subprocess.TimeoutExpired:
            raise TimeoutError("Everything 검색이 시간 초과되었습니다.")
        except Exception as e:
            raise RuntimeError(f"검색 실행 중 오류: {e}")
    
    def _parse_csv(self, csv_path: str) -> List[Dict[str, str]]:
        """CSV 파일 파싱"""
        results = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        return results
    
    def _parse_stdout(self, stdout: str) -> List[Dict[str, str]]:
        """표준 출력 파싱 (간단한 경로 리스트)"""
        results = []
        for line in stdout.strip().split("\n"):
            if line.strip():
                results.append({"path": line.strip()})
        return results
    
    def get_inventory(self, root_path: str, output_dir: str) -> str:
        """
        인벤토리 생성 (주간/월간 리포트용)
        
        Args:
            root_path: 검색할 루트 경로
            output_dir: 출력 디렉토리
        
        Returns:
            생성된 CSV 파일 경로
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d")
        output_file = Path(output_dir) / f"inventory_{timestamp}.csv"
        
        query = f'"{root_path}"'
        self.search(query, export_csv=str(output_file), include_metadata=True)
        
        return str(output_file)


# 사용 예시
if __name__ == "__main__":
    provider = EverythingESCLI()
    
    # PDF 파일 검색
    results = provider.search("*.pdf", max_results=100)
    print(f"검색 결과: {len(results)}개")
    
    # 인벤토리 생성
    inventory_file = provider.get_inventory(
        r"C:\Users\Documents",
        r"_meta\inventory"
    )
    print(f"인벤토리 저장: {inventory_file}")
```

---

## 방법 2: HTTP Server (권장 2순위)

### 특징
- **원격/모바일 조회에 적합**
- RESTful API 제공
- **보안 주의**: 로컬 바인딩 + 인증 필수

### 설정 방법

1. Everything 실행
2. Tools → Options → HTTP Server
3. Enable HTTP server 체크
4. Port 설정 (기본: 8080)
5. **보안**: Allow connections from localhost only 체크
6. **인증 설정** (선택, 권장)

### Python 연동 예시

```python
import requests
from typing import List, Dict, Optional
from urllib.parse import quote

class EverythingHTTPServer:
    """Everything HTTP Server Provider"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Args:
            host: Everything HTTP Server 호스트 (기본: localhost)
            port: 포트 번호 (기본: 8080)
            username: 인증 사용자명 (선택)
            password: 인증 비밀번호 (선택)
        """
        self.base_url = f"http://{host}:{port}"
        self.auth = (username, password) if username and password else None
    
    def search(
        self,
        query: str,
        max_results: int = 1000,
        offset: int = 0
    ) -> List[Dict[str, str]]:
        """
        HTTP API를 통한 검색
        
        Args:
            query: 검색 쿼리
            max_results: 최대 결과 수
            offset: 결과 오프셋
        
        Returns:
            검색 결과 리스트
        """
        url = f"{self.base_url}/?s={quote(query)}&count={max_results}&offset={offset}"
        
        try:
            response = requests.get(
                url,
                auth=self.auth,
                timeout=10
            )
            response.raise_for_status()
            
            # Everything HTTP API는 텍스트 형식으로 결과 반환
            results = []
            for line in response.text.strip().split("\n"):
                if line.strip():
                    results.append({
                        "path": line.strip(),
                        "query": query
                    })
            
            return results[:max_results]
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP Server 요청 실패: {e}")
    
    def health_check(self) -> bool:
        """Everything HTTP Server 연결 상태 확인"""
        try:
            response = requests.get(
                f"{self.base_url}/",
                auth=self.auth,
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# 사용 예시
if __name__ == "__main__":
    # 보안: localhost만 허용, 인증 사용 권장
    provider = EverythingHTTPServer(
        host="localhost",
        port=8080,
        username="admin",  # 선택
        password="secure_password"  # 선택
    )
    
    # 연결 확인
    if not provider.health_check():
        print("Everything HTTP Server에 연결할 수 없습니다.")
        exit(1)
    
    # 검색
    results = provider.search("*.pdf", max_results=100)
    print(f"검색 결과: {len(results)}개")
```

---

## 방법 3: SDK (권장 3순위)

### 특징
- **고성능, 앱 내장용**
- Everything SDK DLL 직접 호출
- C/C++ 기반, Python에서는 ctypes 사용

### Python 연동 예시 (ctypes)

```python
from ctypes import *
from ctypes.wintypes import *
from typing import List, Dict, Optional
from pathlib import Path

class EverythingSDK:
    """Everything SDK Provider (ctypes 기반)"""
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Args:
            dll_path: Everything SDK DLL 경로
        """
        self.dll_path = dll_path or self._find_dll_path()
        if not self.dll_path or not Path(self.dll_path).exists():
            raise FileNotFoundError("Everything SDK DLL을 찾을 수 없습니다.")
        
        try:
            self.dll = WinDLL(self.dll_path)
            self._setup_functions()
        except Exception as e:
            raise RuntimeError(f"SDK 초기화 실패: {e}")
    
    def _find_dll_path(self) -> Optional[str]:
        """Everything SDK DLL 경로 자동 탐색"""
        common_paths = [
            r"C:\Program Files\Everything\SDK\Everything64.dll",
            r"C:\Program Files\Everything\SDK\Everything32.dll",
            r"C:\Tools\Everything\SDK\Everything64.dll",
        ]
        for path in common_paths:
            if Path(path).exists():
                return path
        return None
    
    def _setup_functions(self):
        """SDK 함수 시그니처 설정"""
        # Everything_GetVersion
        self.dll.Everything_GetVersion.restype = DWORD
        
        # Everything_SetSearch
        self.dll.Everything_SetSearch.argtypes = [LPCWSTR]
        self.dll.Everything_SetSearch.restype = BOOL
        
        # Everything_Query
        self.dll.Everything_Query.argtypes = [BOOL]
        self.dll.Everything_Query.restype = BOOL
        
        # Everything_GetNumResults
        self.dll.Everything_GetNumResults.restype = DWORD
        
        # Everything_GetResultPath
        self.dll.Everything_GetResultPath.argtypes = [DWORD, LPWSTR, DWORD]
        self.dll.Everything_GetResultPath.restype = BOOL
    
    def search(self, query: str, max_results: int = 10000) -> List[Dict[str, str]]:
        """
        SDK를 통한 검색
        
        Args:
            query: 검색 쿼리
            max_results: 최대 결과 수
        
        Returns:
            검색 결과 리스트
        """
        # 검색 쿼리 설정
        if not self.dll.Everything_SetSearch(query):
            raise RuntimeError("검색 쿼리 설정 실패")
        
        # 검색 실행
        if not self.dll.Everything_Query(True):  # True = 대기
            raise RuntimeError("검색 실행 실패")
        
        # 결과 수 확인
        num_results = self.dll.Everything_GetNumResults()
        num_results = min(num_results, max_results)
        
        # 결과 수집
        results = []
        MAX_PATH = 260
        path_buffer = create_unicode_buffer(MAX_PATH)
        
        for i in range(num_results):
            if self.dll.Everything_GetResultPath(i, path_buffer, MAX_PATH):
                results.append({
                    "path": path_buffer.value,
                    "index": i
                })
        
        return results
    
    def get_version(self) -> int:
        """Everything 버전 확인"""
        return self.dll.Everything_GetVersion()


# 사용 예시
if __name__ == "__main__":
    try:
        provider = EverythingSDK()
        print(f"Everything 버전: {provider.get_version()}")
        
        results = provider.search("*.pdf", max_results=100)
        print(f"검색 결과: {len(results)}개")
        
    except Exception as e:
        print(f"오류: {e}")
```

---

## 통합 Provider 클래스 (Fallback 지원)

```python
from typing import List, Dict, Optional, Literal
from enum import Enum

class ProviderType(Enum):
    ES_CLI = "es_cli"
    HTTP_SERVER = "http_server"
    SDK = "sdk"
    FALLBACK = "fallback"  # Everything 없이 로컬 스캔

class EverythingProvider:
    """통합 Everything Provider (자동 Fallback)"""
    
    def __init__(self, preferred: Optional[ProviderType] = None):
        """
        Args:
            preferred: 선호하는 Provider (None이면 자동 선택)
        """
        self.provider_type = preferred
        self.provider = None
        self._initialize()
    
    def _initialize(self):
        """Provider 초기화 (우선순위: ES CLI > HTTP > SDK > Fallback)"""
        if self.provider_type == ProviderType.ES_CLI:
            try:
                from everything_integration import EverythingESCLI
                self.provider = EverythingESCLI()
                self.provider_type = ProviderType.ES_CLI
                return
            except:
                pass
        
        if self.provider_type == ProviderType.HTTP_SERVER:
            try:
                from everything_integration import EverythingHTTPServer
                self.provider = EverythingHTTPServer()
                if self.provider.health_check():
                    self.provider_type = ProviderType.HTTP_SERVER
                    return
            except:
                pass
        
        if self.provider_type == ProviderType.SDK:
            try:
                from everything_integration import EverythingSDK
                self.provider = EverythingSDK()
                self.provider_type = ProviderType.SDK
                return
            except:
                pass
        
        # 자동 선택 (우선순위)
        for provider_class in [EverythingESCLI, EverythingHTTPServer, EverythingSDK]:
            try:
                if provider_class == EverythingHTTPServer:
                    provider = provider_class()
                    if not provider.health_check():
                        continue
                else:
                    provider = provider_class()
                self.provider = provider
                self.provider_type = ProviderType[provider_class.__name__.replace("Everything", "").upper()]
                return
            except:
                continue
        
        # Fallback: 로컬 스캔
        from pathlib import Path
        self.provider = LocalScanner()
        self.provider_type = ProviderType.FALLBACK
    
    def search(self, query: str, **kwargs) -> List[Dict[str, str]]:
        """검색 실행"""
        return self.provider.search(query, **kwargs)
    
    def get_status(self) -> Dict[str, str]:
        """Provider 상태 확인"""
        return {
            "type": self.provider_type.value,
            "available": self.provider is not None
        }


# Fallback: 로컬 스캐너 (Everything 없을 때)
class LocalScanner:
    """Everything 없이 로컬 파일 시스템 스캔"""
    
    def search(self, query: str, max_results: int = 10000) -> List[Dict[str, str]]:
        from pathlib import Path
        import fnmatch
        
        # 간단한 패턴 매칭 (실제로는 더 복잡한 로직 필요)
        results = []
        # 예시: 현재 디렉토리만 스캔 (실제로는 재귀 스캔 필요)
        for path in Path(".").rglob("*"):
            if fnmatch.fnmatch(path.name, query.replace("*", "*")):
                results.append({"path": str(path.absolute())})
                if len(results) >= max_results:
                    break
        
        return results
```

---

## 보안 권장사항

### HTTP Server 사용 시
- ✅ **로컬 바인딩만 허용** (localhost/127.0.0.1)
- ✅ **인증 활성화** (username/password)
- ✅ **HTTPS 사용** (가능한 경우)
- ❌ **외부 네트워크 노출 금지**
- ❌ **파일 다운로드 기능 비활성화**

### 일반 권장사항
- Everything은 **Read-only 조회 전용**으로 사용
- 파일 이동/삭제는 **절대 자동화하지 않음**
- 모든 작업은 **Plan → Approve → Apply** 플로우 준수

---

## 참고 자료

- [Everything ES CLI 문서](https://www.voidtools.com/support/everything/command_line_interface/)
- [Everything HTTP Server 문서](https://www.voidtools.com/support/everything/http/)
- [Everything SDK 문서](https://www.voidtools.com/support/everything/sdk/)

---

## 문제 해결

### ES CLI를 찾을 수 없음
- Everything 설치 경로 확인
- 환경 변수 PATH에 추가
- 또는 `es_path` 매개변수로 직접 지정

### HTTP Server 연결 실패
- Everything이 실행 중인지 확인
- Tools → Options → HTTP Server 활성화 확인
- 방화벽 설정 확인

### SDK DLL 로드 실패
- 32bit/64bit 아키텍처 일치 확인
- Visual C++ Redistributable 설치 확인
- DLL 경로 확인
