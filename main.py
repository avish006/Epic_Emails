from app import initialize_services, app

if __name__ == '__main__':
    initialize_services()
    app.run(debug=True, host='0.0.0.0', port=5000)