# Heroku Deployment Guide

This guide explains how to deploy the Synthetic Data Generator (with Gradio frontend and FastAPI backend) to Heroku using a **single Basic dyno**.

## Architecture Overview

This application uses a **single-dyno deployment** where both the Gradio frontend and FastAPI backend run in one Heroku dyno:

- **Frontend**: Gradio web interface mounted at `/gradio`
- **Backend**: FastAPI REST API at `/api/v1/*`
- **Process**: Single uvicorn server running both applications
- **Cost**: One Basic dyno ($7/month as of 2025)
- **Performance**: Low latency (no network calls between frontend/backend)

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://www.heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your project is a git repository
4. **OpenAI API Key**: Required for schema generation

## Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create a New Heroku App

```bash
# Create app with a custom name (or let Heroku generate one)
heroku create your-app-name

# Or without a name:
heroku create
```

### 3. Set Environment Variables

Set your OpenAI API key and other configuration:

```bash
# Required: OpenAI API key
heroku config:set OPENAI_API_KEY=your_openai_api_key_here

# Optional: Enable caching (recommended)
heroku config:set CACHE_ENABLED=true

# Optional: Set log level
heroku config:set LOG_LEVEL=INFO
```

### 4. Deploy to Heroku

```bash
# Add files to git (if not already added)
git add .
git commit -m "Add Gradio frontend and Heroku deployment config"

# Push to Heroku
git push heroku main

# Or if you're on a different branch:
git push heroku your-branch:main
```

### 5. Scale the Dyno

Ensure at least one web dyno is running:

```bash
# For Basic dyno
heroku ps:scale web=1

# Check dyno status
heroku ps
```

### 6. Open Your Application

```bash
# Open in browser
heroku open

# Or manually visit:
# https://your-app-name.herokuapp.com
```

## Accessing Your Application

Once deployed, you can access:

- **Gradio Interface**: `https://your-app-name.herokuapp.com/` or `https://your-app-name.herokuapp.com/gradio`
- **API Documentation**: `https://your-app-name.herokuapp.com/docs`
- **Health Check**: `https://your-app-name.herokuapp.com/health`
- **Cache Stats**: `https://your-app-name.herokuapp.com/api/v1/cache/stats`

## Configuration Files

The deployment uses these configuration files:

### `Procfile`
Tells Heroku how to run your application:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### `runtime.txt`
Specifies the Python version:
```
python-3.12.7
```

### `requirements.txt`
Lists all Python dependencies (Heroku uses this for installation)

## Monitoring and Logs

### View Logs

```bash
# View real-time logs
heroku logs --tail

# View last 500 lines
heroku logs -n 500

# Filter for errors
heroku logs --tail | grep ERROR
```

### Monitor Dyno Performance

```bash
# View dyno status
heroku ps

# View dyno metrics (requires dashboard or CLI plugins)
heroku metrics
```

## Troubleshooting

### Application Crashes

1. **Check logs**: `heroku logs --tail`
2. **Verify environment variables**: `heroku config`
3. **Check dyno status**: `heroku ps`
4. **Restart dyno**: `heroku restart`

### Common Issues

#### Missing OpenAI API Key

**Symptom**: 503 errors when generating datasets

**Solution**: Set the API key
```bash
heroku config:set OPENAI_API_KEY=your_key_here
```

#### Out of Memory (R14 error)

**Symptom**: `R14 - Memory quota exceeded`

**Solution**: Upgrade to a larger dyno or optimize memory usage
```bash
# Upgrade to Standard-1X dyno (512MB RAM)
heroku ps:resize web=standard-1x
```

#### Port Binding Error

**Symptom**: `Error R10 (Boot timeout) -> Web process failed to bind to $PORT`

**Solution**: Ensure `main.py` uses `PORT` environment variable (already configured)

#### Gradio Interface Not Loading

**Symptom**: Gradio interface shows errors or doesn't load

**Solution**:
1. Check if gradio is installed: `heroku run pip list | grep gradio`
2. Check logs for import errors: `heroku logs --tail | grep gradio`
3. Restart the dyno: `heroku restart`

## Updating Your Application

When you make changes:

```bash
# Commit changes
git add .
git commit -m "Your commit message"

# Deploy updates
git push heroku main

# Application will automatically restart
```

## Cost Optimization

### Basic Dyno ($7/month)

- **RAM**: 512 MB
- **CPU**: 1x
- **Sleeps**: No (always on)
- **Best for**: Development, small-scale production

### Performance Tips

1. **Enable caching**: Reduces OpenAI API calls and costs
   ```bash
   heroku config:set CACHE_ENABLED=true
   ```

2. **Limit concurrent requests**: Basic dyno handles ~100 concurrent connections

3. **Monitor usage**: Use Heroku metrics to track performance

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key for schema generation |
| `CACHE_ENABLED` | No | `true` | Enable schema caching |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `PORT` | Auto | - | Set by Heroku automatically |

## Local Testing

Before deploying, test the integrated application locally:

```bash
# Install dependencies
uv sync

# Set environment variables
export OPENAI_API_KEY=your_key_here
export CACHE_ENABLED=true
export LOG_LEVEL=INFO

# Run the application
uv run python main.py

# Access locally:
# - Gradio: http://localhost:8000/gradio
# - API Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

## Production Considerations

### Security

1. **Never commit API keys**: Use environment variables only
2. **CORS Configuration**: Update `main.py` CORS settings for production
3. **HTTPS**: Heroku provides HTTPS automatically

### Performance

1. **Rate Limiting**: Consider adding rate limiting for production
2. **Caching**: Enable caching to reduce API costs and improve performance
3. **Error Monitoring**: Consider adding Sentry or similar service

### Scaling

If you outgrow Basic dyno:

```bash
# Upgrade to Standard-1X (512MB)
heroku ps:resize web=standard-1x

# Upgrade to Standard-2X (1GB)
heroku ps:resize web=standard-2x

# Scale to multiple dynos (not recommended for single-app approach)
heroku ps:scale web=2
```

## Additional Resources

- [Heroku Python Documentation](https://devcenter.heroku.com/categories/python-support)
- [Heroku Dyno Types](https://www.heroku.com/pricing)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gradio Documentation](https://www.gradio.app/docs)

## Support

For issues:
1. Check application logs: `heroku logs --tail`
2. Review this documentation
3. Check Heroku status: [status.heroku.com](https://status.heroku.com)
4. Contact support if needed

---

**Note**: This deployment guide assumes you're using the single-dyno approach where Gradio and FastAPI run together in one process. This is the most cost-effective solution for small to medium traffic applications.
