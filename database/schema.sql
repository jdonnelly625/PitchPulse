-- Create Team table
CREATE TABLE team (
    id INTEGER PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    subreddit VARCHAR(128),
    next_game DATETIME,
    api_id INTEGER
);

-- Create Player table
CREATE TABLE player (
    id INTEGER PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    season_count INTEGER DEFAULT 0,
    team_id INTEGER,
    FOREIGN KEY (team_id) REFERENCES team(id)
);

-- Create Nickname table
CREATE TABLE nickname (
    id INTEGER PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    player_id INTEGER,
    FOREIGN KEY (player_id) REFERENCES player(id)
);
