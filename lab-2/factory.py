from player import Player
import xml.etree.ElementTree as ET
import player_pb2 as pb
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import ParseDict

ELEMENT_NAMES = ["nickname", "email", "date_of_birth", "xp", "class"]


class PlayerFactory:
    def to_json(self, players):
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''
        return [
            {
                "nickname": player.nickname,
                "email": player.email,
                "date_of_birth": str(player.date_of_birth)[:10],
                "xp": player.xp,
                "class": player.cls
            }
            for player in players
        ]

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        return [
            Player(
                data["nickname"],
                data["email"],
                data["date_of_birth"],
                data["xp"],
                data["class"]
            )
            for data in list_of_dict
        ]

    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''
        players = []
        root = ET.fromstring(xml_string)
        for player_elem in root.findall('player'):
            nickname = player_elem.find('nickname').text
            email = player_elem.find('email').text
            date_of_birth = player_elem.find('date_of_birth').text
            xp = int(player_elem.find('xp').text)
            cls = player_elem.find('class').text
            player = Player(nickname, email, date_of_birth, xp, cls)
            players.append(player)
        return players

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''
        root = ET.Element("data")
        for player in list_of_players:
            player_elem = ET.Element("player")
            player_dict = {
                "nickname": player.nickname,
                "email": player.email,
                "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                "xp": str(player.xp),
                "class": player.cls
            }
            for key, value in player_dict.items():
                elem = ET.Element(key)
                elem.text = value
                player_elem.append(elem)
            root.append(player_elem)
        return ET.tostring(root, encoding="utf-8").decode("utf-8")

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        players_list_protobuf = pb.PlayersList()
        players_list_protobuf.ParseFromString(binary)
        players = []
        for player_protobuf in players_list_protobuf.player:
            player_dict = MessageToDict(player_protobuf)
            date_of_birth = player_dict.pop('dateOfBirth', None)
            if date_of_birth:
                player_dict['date_of_birth'] = date_of_birth
            cls = player_dict.get('cls')
            if isinstance(cls, int):
                player_dict['cls'] = pb.Class.Name(cls)
            player = Player(**player_dict)
            players.append(player)
        return players

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects into a binary protobuf string.
        '''
        players_list_protobuf = pb.PlayersList()
        for player in list_of_players:
            player_dict = player.__dict__
            player_dict['date_of_birth'] = player_dict['date_of_birth'].strftime("%Y-%m-%d")
            player_dict['cls'] = pb.Class.Value(player_dict['cls'])
            player_protobuf = players_list_protobuf.player.add()
            ParseDict(player_dict, player_protobuf)
        binary_format = players_list_protobuf.SerializeToString()
        return binary_format