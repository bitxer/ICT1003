from listener import init_app

app = init_app(config="listener.config.Development")

if app:
    try:
        app.run(host="127.0.0.1", port=5000)
    except KeyboardInterrupt:
        print(" [*] Keyboard interrupt detected. Terminating application...")
else:
    print("[!] Couldn't start HTTP Listener. Please see logs for more details.")
