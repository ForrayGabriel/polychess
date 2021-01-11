import requests, json

class Lichess:
    
    def __init__(self):
        """Set initial variables
        """
        self.token = "IFssIxUHfTkxhYcr"
        self.header = {
            "Authorization": "Bearer {}".format(self.token)
        }
        self.firstPlayer = 0
        
    def setGameId(self):
        self.gameId = input('GameId : ')

    def makeMove(self, moveUCI):
        """send request to make move on lichess
        Args:
            moveUCI (string): player movement
        """
        request = requests.post("https://lichess.org/api/bot/game/" + self.gameId + "/move/" + moveUCI, headers=self.header)
        res = json.loads(str(request.text))
        if 'error' in res:
            print(f"Erreur : {res['error']}")
            self.makeMove(input('A toi de jouer : '))
        
    def loadGame(self, res):
        """Inititalisation of the game when we connect to the game
        Args:
            res (dict): data about the game
        """
        if 'id' in res['white']:
            self.firstPlayer = 1
            if len(res['state']['moves']) == 0:
                self.makeMove(input('A toi de jouer le premier coup : '))
            else:
                print('Tu as jouer le premier coup')
                print('Liste des coups effectuées : ' + res['state']['moves'])
        else:
            if len(res['state']['moves']) == 0:
                print('Attend le premier coup de ton adversaire')
            else:
                print('Ton adversaire a joué le premier coup')
                print('Liste des coups effectuées : ' + res['state']['moves'])
            
        moves = res['state']['moves'].split(' ')
        if (len(moves) + self.firstPlayer) % 2 == 1:
            self.makeMove(input('A toi de jouer : '))

    def getStatusGame(self):
        """Get stream of the game, and make action when data is received
        """
        url = f"https://lichess.org/api/bot/game/stream/{self.gameId}"
        s = requests.Session()

        with s.get(url, headers=self.header, stream=True) as resp:
            for line in resp.iter_lines():
                line = line.decode("utf-8")
                if 'id' in line:
                    res = json.loads(line)
                    self.loadGame(res)

                elif 'gameState' in line:
                    res = json.loads(line)
                    moves = res['moves'].split(' ')
                    if (len(moves) + self.firstPlayer) % 2 == 1:
                        print(f"coup de l'adversaire : {moves.pop()}")
                        self.makeMove(input('A toi de jouer : '))

lich = Lichess()
lich.setGameId()
lich.getStatusGame()