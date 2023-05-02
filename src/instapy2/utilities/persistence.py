from datetime import datetime
from time import mktime
from sqlite3 import connect, Connection, Cursor


class Persistence:
    defaults = {
        "medias_comments_hashtag": ["id", "timestamp"],
        "medias_likes_hashtag": ["id", "timestamp"],
    }

    def __open(self) -> Connection:
        return connect(database="data.db")

    def __cursor(self) -> Cursor:
        return self.__open().cursor()

    def __table_exists(self, table: str) -> bool:
        return (
            self.__cursor()
            .execute(f"SELECT name FROM sqlite_master WHERE name='{table}'")
            .fetchone()
            is not None
        )

    def all_identifiers(self, table: str) -> list[str]:
        cursor = self.__cursor()

        tuples = cursor.execute(f"SELECT identifier from {table}").fetchall()
        return [identifier for identifier, in tuples]

    def create_tables(self):
        cursor = self.__cursor()

        for key in self.defaults.keys():
            if not self.__table_exists(table=key):
                keys = self.defaults[key]
                joined_keys = ", ".join(keys)

                cursor.execute(f"CREATE TABLE {key}({joined_keys})")
                cursor.connection.commit()

    def identifier_exists(self, table: str, identifier: str) -> bool:
        cursor = self.__cursor()

        return (
            cursor.execute(
                f"SELECT identifier FROM {table} WHERE identifier='{identifier}'"
            ).fetchone()
            is not None
        )

    def insert_identifier(self, table: str, identifier: str, timestamp: datetime):
        cursor = self.__cursor()

        cursor.execute(
            f"INSERT INTO {table} VALUES (?, ?)",
            (
                identifier,
                mktime(
                    t=timestamp.timetuple(),
                ),
            ),
        )
        cursor.connection.commit()
