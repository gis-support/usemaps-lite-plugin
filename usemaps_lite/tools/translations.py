from qgis.PyQt.QtCore import QSettings


TRANSLATIONS = {
    "error": {
        "login": {"pl": "Błąd logowania", "en": "Login error"},
        "metadata": {"pl": "Błąd pobierania metadanych organizacji", "en": "Error getting organization metadata"},
        "register": {"pl": "Błąd rejestracji", "en": "Register error"},
        "comment": {"pl": "Błąd dodawania komentarza", "en": "Send comment error"},
        "user exists": {"pl": "Zaproszony współpracownik już istnieje w GIS.Box Lite. Każde konto może być przypisane tylko do jednej Organizacji. Poproś współpracownika o usunięcie konta, aby dodać go do swojej organizacji (lub użyj innego adresu e-mail)", "en": "The invited coworker already exists in GIS.Box Lite. Each account can only be assigned to one Organization. Ask the coworker to remove the account to add him to your organization (or use a different email address)"},
        "invite": {"pl": "Błąd wysyłania zaproszenia", "en": "Send invite error"},
        "remove user": {"pl": "Błąd usuwania współpracownika", "en": "Remove coworker error"},
        "load layer": {"pl": "Błąd wczytywania warstwy", "en": "Load layer error"},
        "import layer":  {"pl": "Błąd wgrywania warstwy", "en": "Upload layer error"},
        "remove layer": {"pl": "Błąd usuwania warstwy", "en": "Remove layer error"},
        "edit layer": {"pl": "Błąd edycji warstwy", "en": "Edit layer error"},
        "wrong file format": {"pl": "Zły format pliku. Proszę wybrać plik w formacie .gpkg (GeoPackage)", "en": "Wrong file format. Please select a file in .gpkg (GeoPackage) format"},
        "verification": {"pl": "Błąd weryfikacji", "en": "Verification error"}
    },
    "ui": {
        "info_label": {"pl": 'GIS.Box Lite to darmowa część platformy do współpracy na mapach GIS.Box, Pozwala na łatwą pracę zespołową w QGIS. Dowiedz się więcej na <a href="https://gis-support.pl/gis-box-lite">stronie GIS.Box Lite</a>.', "en": 'GIS.Box Lite is the free version of the GIS.Box platform for collaborative mapping. It enables easy teamwork in QGIS. Learn more on <a href="https://gis-support.pl/gis-box-lite">the GIS.Box Lite website</a>.'},
        "login_button": {"pl": "Zaloguj się", "en": "Login"},
        "register_button": {"pl": "Zarejestruj się", "en": "Register"},
        "user":  {"pl": "Użytkownik", "en": "User"},
        "user_info_label": {"pl": "z organizacji", "en": "from organization"},
        "logout_button": {"pl": "Wyloguj się", "en": "Logout"},
        "events_tab": {"pl": "Powiadomienia", "en": "Notifications"},
        "layers_tab": {"pl": "Dane", "en": "Data"},
        "users_tab": {"pl": "Organizacja", "en": "Organization"},
        "recent_activities_label": {"pl": "Ostatnie aktywności", "en": "Recent activities"},
        "comment_lineedit": {"pl": "Dodaj komentarz...", "en": "Add comment..."},
        "add_comment_button": {"pl": "Wyślij", "en": "Send"},
        "available_layers_label": {"pl": "Dostępne warstwy", "en": "Available layers"},
        "layers_info_label": {"pl": "lista warstw dostępnych dla Twojej organizacji", "en": "list of layers available to Your Organization"},
        "import_layer_button": {"pl": "Dodaj nową warstwę", "en": "Add new layer"},
        "remove_layer_button": {"pl": "Usuń warstwę", "en": "Remove layer"},
        "used_limit_label": {"pl": "Wykorzystany limit", "en": "Used limit"},
        "coworkers": {"pl": "Współpracownicy", "en": "Coworkers"},
        "invite_user_button": {"pl": "Zaproś Współpracownika", "en": "Invite Coworker"},
        "remove_user_button": {"pl": "Usuń Współpracownika", "en": "Remove Coworker"},
        "remove user label": {"pl": "Usunięcie współpracownika", "en": "Remove coworker"},
        "remove user question": {"pl": "Czy na pewno chcesz usunąć współpracownika? Tej operacji nie da się cofnąć", "en": "Are you sure you want to remove the coworker? This operation cannot be undone"},
        "remove layer label": {"pl": "Usunięcie warstwy", "en": "Remove layer"},
        "remove user question": {"pl": "Czy na pewno chcesz usunąć warstwę? Tej operacji nie da się cofnąć", "en": "Are you sure you want to remove the layer? This operation cannot be undone"},
        "invite user title": {"pl": "Zaproś współpracownika", "en": "Invite coworker"},
        "invite user label": {"pl": "W celu zaproszenia współpracownika,  podaj jego e-mail.  Twój współpracownik otrzyma wiadomość z prośbą o weryfikację adresu e-mail.  Po weryfikacji,  dołączy do Twojej organizacji.", "en": "To invite a coworker, enter their email address. Your coworker will receive a message asking them to verify their email address. Once verified, they will join your organization."},
        "invite": {"pl": "Zaproś", "en": "Invite"},
        "cancel": {"pl": "Anuluj", "en": "Cancel"},
        "import layer title": {"pl": "Dodaj nową warstwę", "en": "Add new layer"},
        "select_file_button": {"pl": "Wybierz plik", "en": "Select file"},
        "select_file_label": {"pl": "lub przeciągnij go tutaj (GeoPackage)", "en": "or drop it here (GeoPackage)"},
        "layer_label": {"pl": "Wybierz warstwę", "en": "Select layer"},
        "add": {"pl": "Dodaj", "en": "Add"},
        "login title": {"pl": "Logowanie", "en": "Login"},
        "email_label": {"pl": "Email", "en": "Email"},
        "password_label": {"pl": "Hasło", "en": "Password"},
        "login_button": {"pl": "Zaloguj", "en": "Login"},
        "register title": {"pl": "Rejestracja", "en": "Register"},
        "orgname_label": {"pl": "Nazwa organizacji", "en": "Organization name"},
        "password_again_label": {"pl": "Powtórz hasło", "en": "Repeat password"},
        "register_button": {"pl": "Zarejestruj", "en": "Register"},
        "verify org title": {"pl": "Weryfikacja konta", "en": "Account verification"},
        "verify_label": {"pl": "Na Twój adres e-mail wysłano 6-cyfrowy kod.  Wprowadź go poniżej:","en": "A 6-digit code has been sent to your email address. Please enter it below:"},
        "code_line": {"pl": "Kod weryfikacyjny", "en": "Verification code"},
        "ok": {"pl": "Ok", "en": "Ok"},
        "verified": {"pl": "Zweryfikowany", "en": "Verified"},
        "online": {"pl": "Online", "en": "Online"},
        "select_file": {"pl": "Wybierz plik GeoPackage", "en": "Select GeoPackage file"},
        "file_filter": {"pl": "Plik GeoPackage (*.gpkg)", "en": "GeoPackage file (*.gpkg)"}
        
    },
    "info": {
        "invited user event": {"pl": "zaproszono współpracownika", "en": "invited coworker"},
        "verified user event": {"pl": "zweryfikowano konto", "en": "account verified"},
        "deleted user event": {"pl": "usunięto współpracownika", "en": "removed coworker"},
        "uploaded layer event": {"pl": "dodano warstwę", "en": "added layer"},
        "edited layer event": {"pl": "edytowano warstwę", "en": "edited layer"},
        "added": {"pl": "dodano", "en": "added"},
        "edited": {"pl": "edytowano", "en": "edited"},
        "removed": {"pl": "usunięto", "en": "removed"},
        "deleted layer event": {"pl": "usunięto warstwę", "en": "removed layer"},
        "logged in": {"pl": "Zalogowano się", "en": "Logged in"},
        "invite send": {"pl": "Wysłano zaproszenie", "en": "Invite send"},
        "added new comment": {"pl": "dodał nowy komentarz", "en": "added new comment"},
        "is online": {"pl": "jest online", "en": "is online"},
        "is offline": {"pl": "jest offline", "en": "is offline"},
        "removed layer": {"pl": "usunął warstwę", "en": "removed layer"},
        "added layer": {"pl": "dodał warstwę", "en": "added layer"},
        "edited layer": {"pl": "edytował warstwę", "en": "edited layer"},
        "yes": {"pl": "Tak", "en": "Yes"},
        "no": {"pl": "Nie", "en": "No"}
    }
}

class Translator:
    def __init__(self):
        self.translations = TRANSLATIONS
        self.lang = self._get_locale()

    def _get_locale(self) -> str:
        settings = QSettings()
        locale = settings.value("locale/userLocale", "en")[:2]
        
        if locale != 'pl':
            return 'en'
        
        return locale

    def translate(self, group: str, key: str) -> str:
        
        translation = self.translations[group][key][self.lang]
        
        return translation
        
    def translate_error(self, error_key: str) -> str:

        return self.translate("error", error_key)
    
    def translate_ui(self, ui_key: str) -> str:
        
        return self.translate("ui", ui_key)
    
    def translate_info(self, info_key) -> str:
        
        return self.translate("info", info_key)

TRANSLATOR = Translator()
