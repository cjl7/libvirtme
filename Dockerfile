FROM alpine:3.21.3

RUN apk update && apk add python3 py3-libvirt py3-django
#RUN apk add --no-cache pkg-config libvirt-dev python3

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]