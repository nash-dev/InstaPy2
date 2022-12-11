# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [WIP]
## [0.0.28] - 2022-12-12
### Added
- Added support for Pexels.
    - Pexels requires a query and caption to function.
- Added support for Unsplash.
    - Unsplash does not require a query but does require a caption.
    - Using Unsplash without a query will result in it using a random photo.
- Added support for Emoji.
    
## [Released]
## [0.0.27] - 2022-11-25
### Added
- Added ability to direct message users.
    - Direct messaging is only available through `follow(..., type=FollowType.Users)` and `like(..., type=LikeType.Users)`.

## [0.0.26] - 2022-11-11
### Added
- Added basic implementation to post media.

### Fixed
- Fixed instapy2 has no object medias_tag error.

### Removed
- Removed support for challenge handling.
    - This may not be required through testing.

## [0.0.24] - 2022-11-04
### Added
- Added `comment_locations`.
    - > Please read *Changed* for the changes to `comment_locations`.
- Added basic 2FA support however, Instagram has changed something and it will not work.

### Changed
- Changed `comment_locations` to `comment` with a `type` argument.
- Moved all `like_*` functions to a single `like` function with a `type` argument.
- Moved all `follow_*` functions to a single `follow` function with a `type` argument.
    - `follow` is all self-contained meaning it will call itself for all functionality.
- Improved all imports (x2).

### Fixed
- Fixed an issue in `follow_likers` that would cause a crash.
    - Following users may result in an output: `[ERROR]: Failed to follow user: x`.
        - This may mean the user has a private account and the follow is requested.
        - This will be improved later.

## [0.0.22] - 2022-10-24
### Added
- Added `follow_commenters`, `follow_likers` and `like_locations`.

### Changed
- Changed `medias_username` to stop any chance of causing a crash.

## [0.0.21] - 2022-10-21
### Added
- Added `like_feed`.

### Removed
- Removed interactions from `follow_by_locations` and `follow_by_tags` to match InstaPy.

## [0.0.20] - 2022-10-18
### Added
- Added `like_users`.

### Changed
- Started moving `try:except` calls to their appropriate helper and utility classes.

### Fixed
- Fixed an issue where InstaPy2 would say already following when not attemping to.

## [0.0.19] - 2022-10-15
> Please read **Instagrapi via GitHub** in the README.

### Added
- Added better check for commenting by using `comments_disabled`.

### Changed
- Improved readability of code for `like_tags`.

### Fixed
- Fixed an issue which resulted in a crash and consequent exit of running script.
    - `try:except:` for line 131-135 [like_tags#L131](https://github.com/InstaPy2/InstaPy2/blob/main/instapy2/instapy2.py#L131) courtesy of @vcscsvcscs.

## [0.0.18] - 2022-10-11
### Added
- Added `follow_locations`, `follow_tags` and `follow_usernames`.
- Added `unfollow_users`.
    - Use `amount` to set how many users to unfollow.
    - Use `usernames` to set a custom list of users to unfollow.
    - Use `only_nonfollowers` to only unfollow people who aren't following you.
    - Use `randomize_usernames` to randomly unfollow users.

### Changed
- Renamed the `like` function to `like_tags`.
- Improved handling of detecting relationship status between the session and other users.

## [0.0.17] - 2022-10-08
> Add your settings.json file to **../InstaPy2/instapy2/files/*settings.json*** if you already have one.

### Added
- Added seperate classes for helpers and utilities to clean cluttered code.

### Changed
- Completely overhauled the way configuration is handled with `configuration.` functions.
- Reimplemented `like_by_tags` with the new configuration handler and fixed previous related issues.

## [0.0.16] - 2022-10-02
### Added
- Finished implementation of `like_by_tags` and `like_by_users`.
- Added new enum ProductType to differentiate from the different media types.

### Changed
- Changed the MediaType enum to match with the Instagram media type values.

### Removed
- Removed false imports that may have caused issues.

## [0.0.15] - 2022-09-30
### Added
- Added basic `like_by_users` functionality with support for following.

### Changed
- Modified some existing code to use Union allowing for multiple types within a single parameter.

## [0.0.14] - 2022-09-29
### Added
- Added support for `set_can_follow`.
    - Users can now set whether the bot will follow a user.
        - Configure this option with both `set_can_follow` and `set_friends_to_skip`.

### Changed
- Changed version number to conform with Semantic Versioning (x.y.z, not w.x.y.z).

## [0.0.1.3] - 2022-09-28
### Added
- Added support for `comment_on_liked_media`.
    - Setting `comment_on_liked_media` to `True` will enable commenting for currently parsed and liked media.
    - Media that is not liked will not receive a comment.
        - This will be improved so users can comment on unliked media at a later date.

### Changed
- Created a better `media_passes_all_checks` function to check whether media can be interacted with.
- Moved some functions from [instapy2.py](instapy2.py) to their respective *_util.py files.
    - [comment_util.py](comment_util.py), [like_util.py](like_util.py), etc.
- Changed `media_contains_mandatory_*` from `any()` to `all()`.
    - This change was made to correspond with how InstaPy handles the same check.

### Fixed
- Fixed an issue caused by commenting out the comment and like code.
    - InstaPy2 will now **ACTUALLY** comment and like media based on user configuration.

## [0.0.1.2] - 2022-09-27
### Added
- Implemented most features of `like_by_tags`.
    - `like_by_tags` will now comment on and like media based on the configuration set by you, the user (see [script.py](script.py)).

### Changed
- Improved the way InstaPy2 checks for hashtags, phrases or words within the caption text of media.

### TODO
- Clean up the code and move features into their respective *_util.py files.
- Add the ability to unlike once likes, etc. from InstaPy.

## [0.0.1.1] - 2022-09-27
### Added
- Added basic `like_by_tags` functionality with support for skipping media containing hashtags or phrases.
    - Users can also limit likes to media with a current like count between a given range (only like if media currently has between 0-100 likes).
- Added Pillow requirement to [requirements.txt](requirements.txt)

## [0.0.1] - 2022-09-26
### Added
- Added `like_by_tags` with **very** limited functionality.
    - `like_by_tags` only retrieves media at the moment and does not actually interact with said media.

### Changed
- Changed from Selenium to [Instagrapi](https://github.com/adw0rd/instagrapi).

### Removed
- Removed old InstaPy code in favour of InstaPy2's.

## [0.6.19] - 2022-09-23
No functional changes were made to 0.6.19.