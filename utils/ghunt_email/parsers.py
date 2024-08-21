from utils.ghunt_email.utils import *
from utils.ghunt_email.utils import get_datetime_utc
from utils.ghunt_email.errors import *
from utils.ghunt_email.player.search_player_results_pb2 import PlayerSearchResultsProto
from utils.ghunt_email.player.get_player_response_pb2 import GetPlayerResponseProto

class Parser(SmartObj):
    def _merge(self, obj) -> any:
        """Merging two objects of the same class."""

        def recursive_merge(obj1, obj2, module_name: str) -> any:
            directions = [(obj1, obj2), (obj2, obj1)]
            for direction in directions:
                from_obj, target_obj = direction
                for attr_name, attr_value in from_obj.__dict__.items():
                    class_name = get_class_name(attr_value)
                    if class_name.startswith(module_name) and attr_name in target_obj.__dict__:
                        merged_obj = recursive_merge(attr_value, target_obj.__dict__[attr_name], module_name)
                        target_obj.__dict__[attr_name] = merged_obj

                    elif not attr_name in target_obj.__dict__ or \
                        (attr_value and not target_obj.__dict__.get(attr_name)):
                        target_obj.__dict__[attr_name] = attr_value
            return obj1

        class_name = get_class_name(self)
        module_name = self.__module__
        if not get_class_name(obj).startswith(class_name):
            raise GHuntObjectsMergingError("The two objects being merged aren't from the same class.")

        self = recursive_merge(self, obj, module_name)

class ConferenceProperties(Parser):
    def __init__(self):
        self.allowed_conference_solution_types: List[str] = []

    def _scrape(self, conference_props_data: Dict[str, any]):
        if (types := conference_props_data.get("allowedConferenceSolutionTypes")):
            self.allowed_conference_solution_types = types

class Calendar(Parser):
    def __init__(self):
        self.id: str = ""
        self.summary: str = ""
        self.time_zone: str = ""
        self.conference_properties: ConferenceProperties = ConferenceProperties()

    def _scrape(self, calendar_data: Dict[str, any]):
        self.id = calendar_data.get("id")
        self.summary = calendar_data.get("summary")
        self.time_zone = calendar_data.get("timeZone")
        conference_props_data = calendar_data.get("conferenceProperties")
        if conference_props_data:
            self.conference_properties._scrape(conference_props_data)

class CalendarReminder(Parser):
    def __init__(self):
        self.method: str = ""
        self.minutes: int = 0

    def _scrape(self, reminder_data: Dict[str, any]):
        self.method = reminder_data.get("method")
        self.minutes = reminder_data.get("minutes")

class CalendarPerson(Parser):
    def __init__(self):
        self.email: str = ""
        self.display_name: str = ""
        self.self: bool = None

    def _scrape(self, person_data: Dict[str, any]):
        self.email = person_data.get("email")
        self.display_name = person_data.get("displayName")
        self.self = person_data.get("self")

class CalendarTime(Parser):
    def __init__(self):
        self.date_time: datetime = None # ISO Format
        self.time_zone: str = ""

    def _scrape(self, time_data: Dict[str, any]):
        if (date_time := time_data.get("dateTime")):
            try:
                self.date_time = get_datetime_utc(date_time)
            except ValueError:
                self.date_time = None
        self.time_zone = time_data.get("timeZone")

class CalendarReminders(Parser):
    def __init__(self):
        self.use_default: int = 0
        self.overrides: List[CalendarReminder] = []

    def _scrape(self, reminders_data: Dict[str, any]):
        self.use_default = reminders_data.get("useDefault")
        if (overrides := reminders_data.get("overrides")):
            for reminder_data in overrides:
                reminder = CalendarReminder()
                reminder._scrape(reminder_data)
                self.overrides.append(reminder)

class CalendarEvent(Parser):
    def __init__(self):
        self.id: str = ""
        self.status: str = ""
        self.html_link: str = ""
        self.created: datetime = "" # ISO Format
        self.updated: datetime = "" # ISO Format
        self.summary: str = ""
        self.description: str = ""
        self.location: str = ""
        self.creator: CalendarPerson = CalendarPerson()
        self.organizer: CalendarPerson = CalendarPerson()
        self.start: CalendarTime = CalendarTime()
        self.end: CalendarTime = CalendarTime()
        self.recurring_event_id: str = ""
        self.original_start_time: CalendarTime = CalendarTime()
        self.visibility: str = ""
        self.ical_uid: str = ""
        self.sequence: int = 0
        self.guest_can_invite_others: bool = None
        self.reminders: CalendarReminders = CalendarReminders()
        self.event_type: str = ""

    def _scrape(self, event_data: Dict[str, any]):
        self.id = event_data.get("id")
        self.status = event_data.get("status")
        self.html_link = event_data.get("htmlLink")
        if (date_time := event_data.get("created")):
            try:
                self.created = get_datetime_utc(date_time)
            except ValueError:
                self.created = None
        if (date_time := event_data.get("updated")):
            try:
                self.updated = get_datetime_utc(date_time)
            except ValueError:
                self.updated = None
        self.summary = event_data.get("summary")
        self.description = event_data.get("description")
        self.location = event_data.get("location")
        if (creator_data := event_data.get("creator")):
            self.creator._scrape(creator_data)
        if (organizer_data := event_data.get("organizer")):
            self.organizer._scrape(organizer_data)
        if (start_data := event_data.get("start")):
            self.start._scrape(start_data)
        if (end_data := event_data.get("end")):
            self.end._scrape(end_data)
        self.recurring_event_id = event_data.get("recurringEventId")
        if (original_start_data := event_data.get("originalStartTime")):
            self.original_start_time._scrape(original_start_data)
        self.visibility = event_data.get("visibility")
        self.ical_uid = event_data.get("iCalUID")
        self.sequence = event_data.get("sequence")
        self.guest_can_invite_others = event_data.get("guestsCanInviteOthers")
        if (reminders_data := event_data.get("reminders")):
            self.reminders._scrape(reminders_data)
        self.event_type = event_data.get("eventType")

class CalendarEvents(Parser):
    def __init__(self):
        self.summary: str = ""
        self.updated: datetime = "" # ISO Format
        self.time_zone: str = ""
        self.access_role: str = ""
        self.default_reminders: List[CalendarReminder] = []
        self.next_page_token: str = ""
        self.items: List[CalendarEvent] = []

    def _scrape(self, events_data: Dict[str, any]):
        self.summary = events_data.get("summary")
        if (date_time := events_data.get("updated")):
            try:
                self.updated = get_datetime_utc(date_time)
            except ValueError:
                self.updated = None
        self.time_zone = events_data.get("timeZone")
        self.access_role = events_data.get("accessRole")
        if (reminders_data := events_data.get("defaultReminders")):
            for reminder_data in reminders_data:
                reminder = CalendarReminder()
                reminder._scrape(reminder_data)
                self.default_reminders.append(reminder)
        self.next_page_token = events_data.get("nextPageToken")
        if (items_data := events_data.get("items")):
            for item_data in items_data:
                event = CalendarEvent()
                event._scrape(item_data)
                self.items.append(event)



class PlayerProfile(Parser):
    def __init__(self):
        self.display_name: str = ""
        self.id: str = ""
        self.avatar_url: str = ""
        self.banner_url_portrait: str = ""
        self.banner_url_landscape: str = ""
        self.gamertag: str = ""
        self.last_played_app: PlayerPlayedApp = PlayerPlayedApp()
        self.profile_settings: PlayerProfileSettings = PlayerProfileSettings()
        self.experience_info: PlayerExperienceInfo = PlayerExperienceInfo()
        self.title: str = ""

    def _scrape(self, player_data: Dict[str, any]):
        self.display_name = player_data.get("playerId")
        self.display_name = player_data.get("displayName")
        self.avatar_url = player_data.get("avatarImageUrl")
        self.banner_url_portrait = player_data.get("bannerUrlPortrait")
        self.banner_url_landscape = player_data.get("bannerUrlLandscape")
        self.gamertag = player_data.get("gamerTag")
        if (last_played_app_data := player_data.get("lastPlayedApp")):
            self.last_played_app._scrape(last_played_app_data)
        if (profile_settings_data := player_data.get("profileSettings")):
            self.profile_settings._scrape(profile_settings_data)
        if (experience_data := player_data.get("experienceInfo")):
            self.experience_info._scrape(experience_data)
        self.title = player_data.get("title")

class PlayerPlayedApp(Parser):
    def __init__(self):
        self.app_id: str = ""
        self.icon_url: str = ""
        self.featured_image_url: str = ""
        self.app_name: str = ""
        self.timestamp_millis: str = ""

    def _scrape(self, played_app_data: Dict[str, any]):
        self.app_id = played_app_data.get("applicationId")
        self.icon_url = played_app_data.get("applicationIconUrl")
        self.featured_image_url = played_app_data.get("featuredImageUrl")
        self.app_name = played_app_data.get("applicationName")
        if (timestamp := played_app_data.get("timeMillis")):
            self.timestamp_millis = datetime.utcfromtimestamp(float(timestamp[:10]))

class PlayerExperienceInfo(Parser):
    def __init__(self):
        self.current_xp: str = ""
        self.last_level_up_timestamp_millis: str = ""
        self.current_level: PlayerLevel = PlayerLevel()
        self.next_level: PlayerLevel = PlayerLevel()
        self.total_unlocked_achievements: int = 0

    def _scrape(self, experience_data: Dict[str, any]):
        self.current_xp = experience_data.get("currentExperiencePoints")
        if (timestamp := experience_data.get("lastLevelUpTimestampMillis")):
            self.last_level_up_timestamp_millis = datetime.utcfromtimestamp(float(timestamp[:10]))
        if (current_level_data := experience_data.get("currentLevel")):
            self.current_level._scrape(current_level_data)
        if (next_level_data := experience_data.get("nextLevel")):
            self.next_level._scrape(next_level_data)
        self.total_unlocked_achievements = experience_data.get("totalUnlockedAchievements")

class PlayerLevel(Parser):
    def __init__(self):
        self.level: int = 0
        self.min_xp: str = ""
        self.max_xp: str = ""

    def _scrape(self, level_data: Dict[str, any]):
        self.level = level_data.get("level")
        self.min_xp = level_data.get("minExperiencePoints")
        self.max_xp = level_data.get("maxExperiencePoints")

class PlayerProfileSettings(Parser):
    def __init__(self):
        self.profile_visible: bool = False

    def _scrape(self, profile_settings_data: Dict[str, any]):
        self.profile_visible = profile_settings_data.get("profileVisible")

### Played Applications

class PlayedGames(Parser):
    def __init__(self):
        self.games: List[PlayGame] = []

    def _scrape(self, games_data: Dict[str, any]):
        for game_data in games_data:
            play_game = PlayGame()
            play_game._scrape(game_data)
            self.games.append(play_game)

class PlayGame(Parser):
    def __init__(self):
        self.game_data: PlayGameData = PlayGameData()
        self.market_data: PlayGameMarketData = PlayGameMarketData()
        self.formatted_last_played_time: str = ""
        self.last_played_time_millis: str = ""
        self.unlocked_achievement_count: int = 0

    def _scrape(self, game_data: Dict[str, any]):
        if (games_data := game_data.get("gamesData")):
            self.game_data._scrape(games_data)
        if (market_data := game_data.get("marketData")):
            self.market_data._scrape(market_data)
        self.formatted_last_played_time = game_data.get("formattedLastPlayedTime")
        if (timestamp := game_data.get("lastPlayedTimeMillis")):
            self.last_played_time_millis = datetime.utcfromtimestamp(float(timestamp[:10]))
        self.unlocked_achievement_count = game_data.get("unlockedAchievementCount")

class PlayGameMarketData(Parser):
    def __init__(self):
        self.instances: List[PlayGameMarketInstance] = []

    def _scrape(self, market_data: Dict[str, any]):
        if (instances_data := market_data.get("instances")):
            for instance_data in instances_data:
                instance = PlayGameMarketInstance()
                instance._scrape(instance_data)
                self.instances.append(instance)

class PlayGameMarketInstance(Parser):
    def __init__(self):
        self.id: str = ""
        self.title: str = ""
        self.description: str = ""
        self.images: List[PlayGameImageAsset] = []
        self.developer_name: str = ""
        self.categories: List[str] = []
        self.formatted_price: str = ""
        self.price_micros: str = ""
        self.badges: List[PlayGameMarketBadge] = []
        self.is_owned: bool = False
        self.enabled_features: List[str] = []
        self.description_snippet: str = ""
        self.rating: PlayGameMarketRating = PlayGameMarketRating()
        self.last_updated_timestamp_millis: str = ""
        self.availability: str = ""

    def _scrape(self, instance_data: Dict[str, any]):
        self.id = instance_data.get("id")
        self.title = instance_data.get("title")
        self.description = instance_data.get("description")
        if (images_data := instance_data.get("images")):
            for image_data in images_data:
                image = PlayGameImageAsset()
                image._scrape(image_data)
                self.images.append(image)
        self.developer_name = instance_data.get("developerName")
        self.categories = instance_data.get("categories", [])
        self.formatted_price = instance_data.get("formattedPrice")
        self.price_micros = instance_data.get("priceMicros")
        if (badges_data := instance_data.get("badges")):
            for badge_data in badges_data:
                badge = PlayGameMarketBadge()
                badge._scrape(badge_data)
                self.badges.append(badge)
        self.is_owned = instance_data.get("isOwned")
        self.enabled_features = instance_data.get("enabledFeatures", [])
        self.description_snippet = instance_data.get("descriptionSnippet")
        if (rating_data := instance_data.get("rating")):
            self.rating._scrape(rating_data)
        if (timestamp := instance_data.get("lastUpdatedTimestampMillis")):
            self.last_updated_timestamp_millis = datetime.utcfromtimestamp(float(timestamp[:10]))
        self.availability = instance_data.get("availability")

class PlayGameMarketRating(Parser):
    def __init__(self):
        self.star_rating: float = 0.0
        self.ratings_count: str = ""

    def _scrape(self, rating_data: Dict[str, any]):
        self.star_rating = rating_data.get("starRating")
        self.ratings_count = rating_data.get("ratingsCount")

class PlayGameMarketBadge(Parser):
    def __init__(self):
        self.badge_type: str = ""
        self.title: str = ""
        self.description: str = ""
        self.images: List[PlayGameImageAsset] = []

    def _scrape(self, badge_data: Dict[str, any]):
        self.badge_type = badge_data.get("badgeType")
        self.title = badge_data.get("title")
        self.description = badge_data.get("description")
        if (images_data := badge_data.get("images")):
            for image_data in images_data:
                image = PlayGameImageAsset()
                image._scrape(image_data)
                self.images.append(image)

class PlayGameData(Parser):
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.author: str = ""
        self.description: str = ""
        self.category: PlayGameCategory = PlayGameCategory()
        self.assets: List[PlayGameImageAsset] = []
        self.instances: List[PlayGameInstance] = []
        self.last_updated_timestamp: str = ""
        self.achievement_count: int = 0,
        self.leaderboard_count: int = 0,
        self.enabled_features: List[str] = []
        self.theme_color: str = ""

    def _scrape(self, game_data: Dict[str, any]):
        self.id = game_data.get("id")
        self.name = game_data.get("name")
        self.author = game_data.get("author")
        self.description = game_data.get("description")
        if (category_data := game_data.get("category")):
            self.category._scrape(category_data)
        if (assets_data := game_data.get("assets")):
            for asset_data in assets_data:
                asset = PlayGameImageAsset()
                asset._scrape(asset_data)
                self.assets.append(asset)
        if (instances_data := game_data.get("instances")):
            for instance_data in instances_data:
                instance = PlayGameInstance()
                instance._scrape(instance_data)
                self.instances.append(instance)
        if (timestamp := game_data.get("lastUpdatedTimestamp")):
            self.last_updated_timestamp = datetime.utcfromtimestamp(float(timestamp[:10]))
        self.achievement_count = game_data.get("achievement_count")
        self.leaderboard_count = game_data.get("leaderboard_count")
        self.enabled_features = game_data.get("enabledFeatures", [])
        self.theme_color = game_data.get("themeColor")

class PlayGameInstance(Parser):
    def __init__(self):
        self.platform_type: str = ""
        self.name: str = ""
        self.turn_based_play: bool = False
        self.realtime_play: bool = False
        self.android_instance: List[PlayGameAndroidInstance] = []
        self.acquisition_uri: str = ""

    def _scrape(self, instance_data: Dict[str, any]):
        self.platform_type = instance_data.get("plateformType")
        self.name = instance_data.get("name")
        self.turn_based_play = instance_data.get("turnBasedPlay")
        self.realtime_play = instance_data.get("realtimePlay")
        if (android_instance_data := instance_data.get("androidInstance")):
            android_instance = PlayGameAndroidInstance()
            android_instance._scrape(android_instance_data)
            self.android_instance.append(android_instance_data)

class PlayGameAndroidInstance(Parser):
    def __init__(self):
        self.package_name: str = ""
        self.enable_piracy_check: bool = False
        self.preferred: bool = False

    def _scrape(self, android_instance_data: Dict[str, any]):
        self.package_name = android_instance_data.get("packageName")
        self.enable_piracy_check = android_instance_data.get("enablePiracyCheck")
        self.preferred = android_instance_data.get("preferred")

class PlayGameImageAsset(Parser):
    def __init__(self):
        self.name: str = ""
        self.width: str = ""
        self.height: str = ""
        self.url: str = ""

    def _scrape(self, image_data: Dict[str, any]):
        self.name = image_data.get("name")
        self.width = image_data.get("width")
        self.height = image_data.get("height")
        self.url = image_data.get("url")

class PlayGameCategory(Parser):
    def __init__(self):
        self.primary: str = ""

    def _scrape(self, category_data: Dict[str, any]):
        self.primary = category_data.get("primary")

### Achievements

class PlayerAchievements(Parser):
    def __init__(self):
        self.achievements: List[PlayerAchievement] = []

    def _scrape(self, achievements_data: Dict[str, any]):
        achievements_defs : List[PlayerAchievementDefinition] = []
        if (achievement_defs_data := achievements_data.get("definitions")):
            for achievement_def_data in achievement_defs_data:
                achievement_def = PlayerAchievementDefinition()
                achievement_def._scrape(achievement_def_data)
                achievements_defs.append(achievement_def)
        if (achievements_items_data := achievements_data.get("items")):
            for achievement_item_data in achievements_items_data:
                achievement = PlayerAchievement()
                achievement._scrape(achievement_item_data)
                for achievement_def in achievements_defs:
                    if achievement_def.id == achievement.id:
                        achievement.definition = achievement_def
                self.achievements.append(achievement)

class PlayerAchievement(Parser):
    def __init__(self):
        self.id: str = ""
        self.achievement_state: str = ""
        self.last_updated_timestamp: datetime = 0
        self.app_id: str = 0
        self.xp: str = ""
        self.definition: PlayerAchievementDefinition = PlayerAchievementDefinition()

    def _scrape(self, achievement_item_data: Dict[str, any]):
        self.id = achievement_item_data.get("id")
        self.achievement_state = achievement_item_data.get("achievementState")
        if (timestamp := achievement_item_data.get("lastUpdatedTimestamp")):
            self.last_updated_timestamp = datetime.utcfromtimestamp(float(timestamp[:10]))
        self.app_id = achievement_item_data.get("application_id")
        self.xp = achievement_item_data.get("experiencePoints")

class PlayerAchievementDefinition(Parser):
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.description: str = ""
        self.achievement_type: str = ""
        self.xp: str = ""
        self.revealed_icon_url: str = ""
        self.unlocked_icon_url: str = ""
        self.initial_state: str = ""
        self.is_revealed_icon_url_default: bool = False
        self.is_unlocked_icon_url_default: bool = False
        self.rarity_percent: float = 0.0

    def _scrape(self, achievement_def_data: Dict[str, any]):
        self.id = achievement_def_data.get("id")
        self.name = achievement_def_data.get("name")
        self.description = achievement_def_data.get("description")
        self.achievement_type = achievement_def_data.get("achievementType")
        self.xp = achievement_def_data.get("experiencePoints")
        self.revealed_icon_url = achievement_def_data.get("revealedIconUrl")
        self.unlocked_icon_url = achievement_def_data.get("unlockedIconUrl")
        self.initial_state = achievement_def_data.get("initialState")
        self.is_revealed_icon_url_default = achievement_def_data.get("isRevealedIconUrlDefault")
        self.is_unlocked_icon_url_default = achievement_def_data.get("isUnlockedIconUrlDefault")
        self.rarity_percent = achievement_def_data.get("rarityParcent")

### Global

class Player(Parser):
    def __init__(self, profile: PlayerProfile = PlayerProfile(),
                played_games: List[PlayGame] = [],
                achievements: List[PlayerAchievement] = []):
        self.profile: PlayerProfile = profile
        self.played_games: List[PlayGame] = played_games
        self.achievements: List[PlayerAchievement] = achievements


class PlayerSearchResult(Parser):
    def __init__(self):
        self.name: str = ""
        self.id: str = ""
        self.avatar_url: str = ""

    def _scrape(self, player_result_data):
        self.name = player_result_data.account.name
        self.id = player_result_data.account.id
        self.avatar_url = player_result_data.avatar.url

class PlayerSearchResults(Parser):
    def __init__(self):
        self.results: List[PlayerSearchResult] = []

    def _scrape(self, proto_results: PlayerSearchResultsProto):
        for player_result_data in proto_results.field1.results.field1.field1.player:
            player_search_result = PlayerSearchResult()
            player_search_result._scrape(player_result_data)
            self.results.append(player_search_result)

class PlayerProfile(Parser):
    """
        This parsing is not complete at all, we only use it
        in GHunt to dump total played games & achievements.
    """
    def __init__(self):
        self.achievements_count: int = 0
        self.played_games_count: int = 0

    def _scrape(self, proto_results: GetPlayerResponseProto):
        for section in proto_results.field1.results.section:
            if section.field3.section_name == "Games":
                self.played_games_count = int(section.counter.number)
            elif section.field3.section_name == "Achievements":
                self.achievements_count = int(section.counter.number)