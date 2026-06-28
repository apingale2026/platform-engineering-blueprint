#stage1 builder_stage
FROM python:3.10-alpine AS builder
WORKDIR /app
#copy dependency file
COPY requirements.txt .
# Install dependencies 
RUN pip install --no-cache-dir --user -r requirements.txt

#stage2 as Runner 
FROM python:3.10-alpine AS Runner
WORKDIR /app 
# Create user without password
RUN adduser -D appuser
#copy required dependency build in appuser home directory
COPY --from=builder /root/.local /home/appuser/.local
# set permission of user home directory
RUN chown -R appuser:appuser /home/appuser/.local 
ENV PATH=/home/appuser/.local/bin:$PATH
# set non-root user as appuser
USER appuser 
# copy application content 
COPY app.py .
# Expose port 5001
EXPOSE 5001
# default executable command 
CMD [ "python", "app.py" ]

