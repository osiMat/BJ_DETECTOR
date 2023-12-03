{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5def457c-1cd2-4c57-ab5a-03b738da3b3f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n",
    "import torch\n",
    "from pathlib import Path\n",
    "import requests\n",
    "\n",
    "class BlackjackDetector:\n",
    "    \"\"\"Klasa do detekcji kart i obliczania wyników w grze blackjack.\"\"\"\n",
    "    \n",
    "    def __init__(self, model_url, camera_url, wait_time=5):\n",
    "        self.model_url = model_url\n",
    "        self.droidcam_url = camera_url\n",
    "        self.model = self.download_model(model_url)\n",
    "        self.wait_time = wait_time\n",
    "        self.setup_roi()\n",
    "\n",
    "    def download_model(self, model_url):\n",
    "        model_path = Path(\"models/best.pt\")\n",
    "        if not model_path.is_file():\n",
    "            model_path.parent.mkdir(parents=True, exist_ok=True)\n",
    "            response = requests.get(model_url)\n",
    "            response.raise_for_status()\n",
    "            with open(model_path, 'wb') as f:\n",
    "                f.write(response.content)\n",
    "        return torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)\n",
    "\n",
    "    def setup_roi(self):\n",
    "        \"\"\"Konfiguracja regionów zainteresowania (ROI) dla każdego gracza i krupiera.\"\"\"\n",
    "        self.roi = {\n",
    "            'player1': self.convert_to_roi_tuple([(200, 70), (368, 108), (78, 236), (266, 294)]),\n",
    "            'player2': self.convert_to_roi_tuple([(368, 108), (544, 147), (266, 294), (471, 355)]),\n",
    "            'player3': self.convert_to_roi_tuple([(544, 147), (771, 202), (471, 355), (755, 444)]),\n",
    "            'dealer': self.convert_to_roi_tuple([(68, 251), (753, 466), (2, 354), (695, 594)])\n",
    "        }\n",
    "\n",
    "    @staticmethod\n",
    "    def convert_to_roi_tuple(roi):\n",
    "        \"\"\"Konwersja współrzędnych ROI na krotkę.\"\"\"\n",
    "        x_min = min(point[0] for point in roi)\n",
    "        y_min = min(point[1] for point in roi)\n",
    "        x_max = max(point[0] for point in roi)\n",
    "        y_max = max(point[1] for point in roi)\n",
    "        return (x_min, y_min, x_max, y_max)\n",
    "\n",
    "    @staticmethod\n",
    "    def is_inside_roi(box, roi):\n",
    "        \"\"\"Sprawdzenie, czy dany obszar (box) znajduje się wewnątrz ROI.\"\"\"\n",
    "        x_min, y_min, x_max, y_max = box\n",
    "        roi_x_min, roi_y_min, roi_x_max, roi_y_max = roi\n",
    "        return (x_min >= roi_x_min and y_min >= roi_y_min and x_max <= roi_x_max and y_max <= roi_y_max)\n",
    "\n",
    "    @staticmethod\n",
    "    def is_corner_inside_main_card(corner_box, main_card_box):\n",
    "        \"\"\"Sprawdzenie, czy róg karty znajduje się wewnątrz głównej karty.\"\"\"\n",
    "        corner_x_min, corner_y_min, corner_x_max, corner_y_max = corner_box\n",
    "        main_x_min, main_y_min, main_x_max, main_y_max = main_card_box\n",
    "        return (corner_x_min >= main_x_min and corner_y_min >= main_y_min and corner_x_max <= main_x_max and corner_y_max <= main_y_max)\n",
    "\n",
    "    @staticmethod\n",
    "    def calculate_score(cards):\n",
    "        \"\"\"Oblicza wynik na podstawie listy kart.\"\"\"\n",
    "        values = {'j': 10, 'q': 10, 'k': 10, 'a': 11}\n",
    "        score, aces = 0, 0\n",
    "        for card in cards:\n",
    "            if card in values:\n",
    "                score += values[card]\n",
    "            else:\n",
    "                score += int(card)\n",
    "            if card == 'a':\n",
    "                aces += 1\n",
    "    \n",
    "        while score > 21 and aces:\n",
    "            score -= 10\n",
    "            aces -= 1\n",
    "    \n",
    "        return score\n",
    "\n",
    "\n",
    "    @staticmethod\n",
    "    def determine_result(players_scores, dealer_score):\n",
    "        \"\"\"Ustalenie wyniku gry na podstawie punktów graczy i krupiera.\"\"\"\n",
    "        results = {}\n",
    "        for player, score in players_scores.items():\n",
    "            if score == 21 and len(players_scores[player]) == 2:\n",
    "                results[player] = \"BLACKJACK\"\n",
    "            elif score > 21:\n",
    "                results[player] = \"za dużo\"\n",
    "            else:\n",
    "                if dealer_score > 21 or (score <= 21 and score > dealer_score):\n",
    "                    results[player] = \"wygrana\"\n",
    "                elif score == dealer_score:\n",
    "                    results[player] = \"remis\"\n",
    "                else:\n",
    "                    results[player] = \"przegrana\"\n",
    "        return results\n",
    "\n",
    "    def run_detection(self):\n",
    "        \"\"\"Uruchomienie procesu detekcji kart i obliczania wyników.\"\"\"\n",
    "        cap = cv2.VideoCapture(self.droidcam_url)\n",
    "        \n",
    "        continue_detection = True\n",
    "    \n",
    "        while continue_detection:\n",
    "            ret, frame = cap.read()\n",
    "            if not ret:\n",
    "                print(\"Nie udało się uzyskać obrazu z kamery.\")\n",
    "                break\n",
    "    \n",
    "            frame = cv2.resize(frame, (800, 600))\n",
    "            results = self.model(frame)\n",
    "            results.render()\n",
    "            player_cards = self.detect_cards(results)\n",
    "    \n",
    "            players_scores = self.calculate_players_scores(player_cards)\n",
    "            self.display_results(players_scores)\n",
    "    \n",
    "            key = cv2.waitKey(0)\n",
    "            break\n",
    "\n",
    "    \n",
    "        cap.release()\n",
    "        cv2.destroyAllWindows()\n",
    "\n",
    "\n",
    "    def detect_cards(self, results):\n",
    "        \"\"\"Detekcja kart dla każdego gracza i krupiera.\"\"\"\n",
    "        player_cards = {player: [] for player in self.roi}\n",
    "        for *xyxy, conf, cls in results.xyxy[0]:\n",
    "            box = [int(x) for x in xyxy]\n",
    "            card_label = results.names[int(cls)]\n",
    "            for player, roi in self.roi.items():\n",
    "                if self.is_inside_roi(box, roi):\n",
    "                    player_cards[player].append((box, card_label))\n",
    "                    break\n",
    "        return player_cards\n",
    "\n",
    "    def calculate_players_scores(self, player_cards):\n",
    "        \"\"\"Obliczenie wyników dla każdego gracza.\"\"\"\n",
    "        players_scores = {}\n",
    "        for player, cards in player_cards.items():\n",
    "            identified_cards = self.identify_cards(cards)\n",
    "            score = self.calculate_score(identified_cards)\n",
    "            players_scores[player] = score\n",
    "            self.display_player_cards(player, identified_cards, score)\n",
    "        dealer_score = players_scores.pop('dealer')\n",
    "        return self.determine_result(players_scores, dealer_score)\n",
    "\n",
    "    def identify_cards(self, cards):\n",
    "        \"\"\"Identyfikacja kart na podstawie detekcji.\"\"\"\n",
    "        identified_cards = []\n",
    "        for main_box, main_label in cards:\n",
    "            if main_label.isdigit() or main_label in ['j', 'q', 'k', 'a']:\n",
    "                valid_corners = [corner_label for corner_box, corner_label in cards if corner_label.startswith(main_label) and self.is_corner_inside_main_card(corner_box, main_box)]\n",
    "                if valid_corners:\n",
    "                    identified_cards.append(main_label)\n",
    "        return identified_cards\n",
    "\n",
    "    def display_player_cards(self, player, cards, score):\n",
    "        \"\"\"Wyświetlanie kart i wyniku danego gracza.\"\"\"\n",
    "        result_str = ', '.join(cards)\n",
    "        result_str += \" - wynik: \" + (\"BLACKJACK\" if score == 21 and len(cards) == 2 else str(score))\n",
    "        if score > 21:\n",
    "            result_str += \", za dużo\"\n",
    "        print(f\"{player.capitalize()} posiada karty: {result_str}\")\n",
    "\n",
    "    def display_results(self, players_scores):\n",
    "        \"\"\"Wyświetlanie końcowych wyników gry.\"\"\"\n",
    "        for player, result in players_scores.items():\n",
    "            print(f\"{player.capitalize()}: {result}\")\n",
    "\n",
    "detector = BlackjackDetector('https://github.com/osiMat/BJ_DETECTOR/raw/main/models/best.pt', 'http://192.168.8.100:4747/video')\n",
    "detector.run_detection()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.18"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
