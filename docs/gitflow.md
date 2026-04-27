# Git Flow

This project uses a simple two-stage merge flow:

1. All feature branches are merged into `dev` first.
2. After validation on `dev`, changes are merged into `main`.

## Branch Roles

- `feature/*`: Development branches for new features, fixes, or improvements.
- `dev`: Integration branch for testing and review of incoming work.
- `main`: Production branch used for package deployment.

## Standard Workflow

1. Create a feature branch from `dev`.
2. Open a pull request from `feature/*` to `dev`.
3. Validate changes on `dev` (review, checks, and testing).
4. Open a pull request from `dev` to `main`.
5. Merge to `main` to trigger package deployment.

## Rule

Do not merge feature branches directly into `main`.
