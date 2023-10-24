from myapp import create_backend

app = create_backend()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)