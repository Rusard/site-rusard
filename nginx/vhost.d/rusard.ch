location /static/ {
    alias /home/app/web/staticfiles/;
}

location /media/ {
    alias /home/app/web/mediafiles/;
}
