# Blackjack Card Detector

## Opis
Projekt `Blackjack Card Detector` jest narzędziem do detekcji kart w grze blackjack wykorzystującym model YOLOv5. Skrypt analizuje obraz z kamery w czasie rzeczywistym, rozpoznaje karty na stole i oblicza wyniki dla graczy i krupiera.

## Funkcje
- Detekcja kart blackjack za pomocą kamery.
- Obliczanie wyników gry na podstawie rozpoznanych kart.
- Wykorzystanie modelu YOLOv5 do detekcji obiektów.

## Wymagania
- Python 3.8 lub nowszy
- Biblioteki: `torch`, `cv2`, `pathlib`, `requests` (do pobrania modelu, jeśli nie jest dostępny lokalnie)

## Instalacja
Aby uruchomić projekt, wykonaj następujące kroki:

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/osiMat/BJ_DETECTOR.git
   cd BJ_DETECTOR

2. zainstaluj wymagane zależności:
   ```bash
   pip install torch opencv-python requests

## Użycie
Aby uruchomić detektor kart, wykonaj skrypt blackjack_detector.py. Upewnij się, że podajesz poprawny URL kamery i ścieżkę do modelu YOLOv5. Model możesz pobrać za pomocą linku w folderze 'models'
   ```from blackjack_detector import BlackjackDetector

   # URL modelu (może być lokalny lub zdalny)
   model_url = 'path_to_your_model/best.pt'

   # URL kamery
   camera_url = 'your_camera_url'

   # Tworzenie instancji detektora
   detector = BlackjackDetector(model_url, camera_url)

   # Uruchomienie detekcji
   detector.run_detection()

## Konfiguracja
- Możesz dostosować ROI (Regiony Zainteresowania) dla każdego z graczy i krupiera w metodzie setup_roi.
- Zmodyfikuj model_url i camera_url w skrypcie blackjack_detector.py zgodnie z Twoim środowiskiem i potrzebami.
- Model został stworzony w specyficznie ustalonych warunkach (pozycja kamery, oświetlenie, konkretna talia kart). W innych warunkach model może nie otrzymywać rządanych rezultatów.

## Licencja

Projekt "Blackjack Detector" jest udostępniony na licencji MIT. Oznacza to, że możesz używać, kopiować, modyfikować, łączyć, publikować, dystrybuować, sublicencjonować i/lub sprzedawać kopie oprogramowania, pod warunkiem dołączenia powyższej informacji o prawach autorskich i niniejszego zapisu o licencji we wszystkich kopiach lub istotnych częściach oprogramowania.

Pełny tekst licencji znajdziesz w pliku `LICENSE` dołączonym do tego projektu.


