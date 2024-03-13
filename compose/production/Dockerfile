FROM apache/airflow:2.8.0 as airflow

FROM airflow

ARG BUILD_ENVIRONMENT=production

# # Install apt packages
# RUN apt-get update && apt-get install --no-install-recommends -y \
#     # dependencies for building Python packages
#     build-essential \
#     # psycopg2 dependencies
#     libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN bash -c "pip wheel -r ${BUILD_ENVIRONMENT}.txt"


ENV PYTHONPATH="/opt/airflow:$PYTHONPATH"