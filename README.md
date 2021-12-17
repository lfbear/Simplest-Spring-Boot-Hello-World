# A DevOps design and implementation For `Simplest-Spring-Boot-Hello-World`

## Files description

- [`README.md`](README.md): Design document
- [`Dockerfile`](Dockerfile) & [`run_dockerfile`](run_dockerfile): Static and dynamic Dockerfile
- [`.github/workflows`](.github/workflows): CI/CD config files for github
- [`infra/myapp.py`](infra/myapp.py): AWS CKD scripts for creating the infrastructure


## Design

### Overall

```flow
┌────CI/CD────────────────────────────────────────────────────────────────────┐
│                                                                             │

                 push    ┌───────────┐
              ┌────────► │ unit test │
┌──────────┐  │          └───────────┘                                    ┌──VPC───────────────────┐
│   code   │ ─┤                                                           │                        │  ┌──────────┐
└──────────┘  │           ┌─────────┐        ┌────────────┐               │   ┌─ECS─────────┐      │  │CloudWatch│
              └────────►  │  build  │ ──────►│   deploy   │ ─────┐        │   │             │      │  └──────────┘
                  PR      └─────────┘        └────────────┘      ▼        │   │  ┌───────┐  │      │
                                                              ┌─────┐ ────┼───┼─►│  app  │  │      │
                               │                    ┌───────► │ CDK │     │   │  └───────┘  │      │
                               └─Dockerfile─┐       │         │     │ ───►│   │             │      │
                                            │       │         └─────┘     │   │             │      │
                                            ▼                    ▲        │   │             │      │
                                   ┌──────────────────┐          │        │   └─────────────┘      │
                                   │ Docker registry  │          │        │                        │
                                   │    (artifact)    │          │        │                        │
                                   └──────────────────┘          │        └────────────────────────┘

                                                          ┌────────────┐         On Cloud(AWS)
                                                          │ infra init │
                                                          └────────────┘

                                                         │                                             │
                                                         └─────────────────────────────────────────────┘
                                                                   Infrastructure management
```

### 详细说明

- CI部分: dockerfile

  + 采用多阶段构建，将构建环境和产物环境分开
  + 辅助脚本 `run_dockerfile`，在pom.xml中制品或版本号变更时可以动态渲染docker build所需参数
  + 单元测试：借助于github action，在push或者PR创建时进行单元测试验证

- 基础设施： AWS CDK
  + 通过创建VPC，Cluster，TaskDefinition，LogGroup，FargateService资源创建serverless所需基础设施
  + 通过创建Metric，SNS Topic,Alarm等资源完成使用cloudwatch功能发送报警邮件

- CD部分：
  + 借助github action，在PR合并时进行镜像构建和发布（含基础实施创建）
---

# Simplest-Spring-Boot-Hello-World
Simplest Spring Boot Hello World Example 


# Steps

> git clone https://github.com/goxr3plus/Simplest-Spring-Boot-Hello-World.git

> Run from your favourite IDE ( Eclipse , IntelliJ , Netbeans )

ENJOY THE POWER OF A HELLO WORLD ! Welcome to Spring Boot :)
