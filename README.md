# iRacing Stint Tracker Backend

A lightweight backend service for recording and analyzing endurance racing telemetry from iRacing.  
Built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL (Supabase)** — deployed serverlessly on **AWS Lambda** via **API Gateway**.

---

## Overview

This app powers a personal race engineering tool that tracks key race metrics over time.  
It records **stints**, **laps**, **pit stops**, and **session metadata**, and is designed to evolve into a live race analysis platform with real-time WebSocket support.


Currently, the backend is built for use by my own iRacing team, but future updates will extend functionality to support multiple teams and shared event data.

**Current features**
- Record detailed **stint**, **lap**, and **pit stop** data.
- Manage **sessions** for races and practice events.
- RESTful API built with **FastAPI**.
- Persistent storage using **Supabase (PostgreSQL)**.
- Automatic deployment to **AWS Lambda** via **GitHub Actions**.

**Planned features**
- CSV export for offline analysis.
- WebSocket support for **live race telemetry and strategy tools**.
- User and team authentication

---

## Tech Stack

| Component        | Technology                      |
|------------------|----------------------------------|
| Framework        | FastAPI                          |
| ORM              | SQLAlchemy                       |
| Database         | PostgreSQL (Supabase)             |
| Hosting          | AWS Lambda + API Gateway          |
| Deployment       | GitHub Actions CI/CD              |
| Language         | Python 3.13+                      |

