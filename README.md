# A DevOps design and implementation For `Simplest-Spring-Boot-Hello-World`

## Files description

- [`README.md`](README.md): Design document
- [`Dockerfile`](Dockerfile) & [`run_dockerfile`](run_dockerfile): Static and dynamic Dockerfile
- [`.github/workflows`](.github/workflows): CI/CD config files for github
- [`infra`](infra): AWS CKD scripts for creating the infrastructure


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

### Details

- CI Part: dockerfile

  + Multistage build, separate build image and runtime image
  + Script `run_dockerfile`，dynamicly call `docker build` by rendering parms from pom.xml for 'Dockerfile'
  + Unit test：with github action，trigger at `push event` and `PR open`

- Infrastructure: AWS CDK
  + Creating VPC，Cluster，TaskDefinition，LogGroup，FargateService etc. for Serverless
  + Creating Metric，SNS Topic,Alarm with cloudwatch to send warnning email

- CD Part:
  + Setting applcation name and version in [infra/app.py](infra/app.py) ([CDK Usage](infra/README.md))
  + with github action，trigger deployment at `PR closed`
---

# Simplest-Spring-Boot-Hello-World
Simplest Spring Boot Hello World Example 


# Steps

> git clone https://github.com/goxr3plus/Simplest-Spring-Boot-Hello-World.git

> Run from your favourite IDE ( Eclipse , IntelliJ , Netbeans )

ENJOY THE POWER OF A HELLO WORLD ! Welcome to Spring Boot :)
