from pitch import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


"""
Add this to terminal before you start the app

export SECRET_KEY=df84a75c801a375f226ab9fd83b82a
export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

"""