import goal_tracker

if __name__ == '__main__':
    app = goal_tracker.create_app()
    app.run(debug=True)
