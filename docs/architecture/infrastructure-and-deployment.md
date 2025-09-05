# Infrastructure and Deployment

## Infrastructure as Code

- **Tool:** Not applicable for MVP (local deployment only)
- **Location:** N/A
- **Approach:** Manual local setup, infrastructure as code deferred to post-MVP

## Deployment Strategy

- **Strategy:** Local development deployment via uvicorn
- **CI/CD Platform:** Not implemented for MVP (manual testing approach)
- **Pipeline Configuration:** N/A for MVP scope

## Environments

- **Development:** Local developer machine with uvicorn server - Full functionality including OpenAI API access and file-based caching
- **Production:** Not defined for MVP - Future consideration for educational platform integration

## Environment Promotion Flow

```
Development (Local) → [Future: Staging] → [Future: Production]
```

## Rollback Strategy

- **Primary Method:** Git revert to previous working commit
- **Trigger Conditions:** Service failures, API integration issues, or cache corruption
- **Recovery Time Objective:** <5 minutes (restart local server)
