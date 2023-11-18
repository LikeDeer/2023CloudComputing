# AWS 동적 자원 관리 프로그램

---

### Dependency
필요 패키지들을 설치하려면 아래 명령을 실행하십시오.

`pip install -r requirements.txt`


### Configuring Credentials
`./resources/credentials/` 에 `credentials.scv` 파일을 추가해야
AWS EC2 에 권한을 갖고 정상적으로 연결할 수 있습니다.

CSV 파일은 다음과 같은 형식을 갖고 있습니다.

| Access key ID        | Secret Access key        |
|----------------------|--------------------------|
| 'your access key id' | 'your secret access key' |

**IAM User** 를 생성하고 **Security credentials** 메뉴의 **Access keys** 항목에서
'Create Access Key' 를 통해 키를 생성하고 'Download .csv' 버튼을 눌러 파일을 생성하세요.
 그 후 이름을 'credentials.csv'로 변경 후 아래와 같은 정확한 경로에 추가하세요. _(노출에 주의하세요)_

```
.
├── modules
├── resources
│   └── credentials
│       └── credentials.csv
└── venv
```