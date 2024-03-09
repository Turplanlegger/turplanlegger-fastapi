import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User SQLModel
    Attributes:
        id (str): UUID of the user
        name (str): First name of the user
        last_name (str): Last name/sir name of the user
        email (str): Email of the user
        private (bool): Flag if the user should be private or public
                        Default: False
        deleted (bool): Flag if the user has logically been deleted
        delete_time (datetime): Time of the deletion of the user
        create_time (datetime): Time of creation,
                                Default: datetime.now()
    """
    __tablename__ = 'users'
    id: uuid.UUID = Field(
    default_factory=uuid.uuid4,
    primary_key=True,
    index=True,
    nullable=False,
    description='ID of the user as UUID'
    )
    first_name: str = Field(
    sa_column=Column(
        type_=TEXT,
        nullable=False
    )
    )
    last_name: str = Field(
    sa_column=Column(
        type_=TEXT,
        nullable=False
    )
    )
    email: str = Field(
    sa_column=Column(
        type_=TEXT,
        nullable=False
    )
    )
    private: bool = False
    create_time: datetime = datetime.now(UTC)
    deleted: Optional[bool] = False
    delete_time: Optional[datetime]


# class Routes(SQLModel, table=True):
#   __tablename__ = "routes"
#   id: Optional[int] = Field(default=None, primary_key=True)
#   route: JSON
#   route_history: JSON
#   name: str
#   comment: str
#   owner: str = Field(foreign_key="users.id")
#   create_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
#   deleted: bool = Field(default=False)
#   delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# class Item_Lists(SQLModel, table=True):
#   __tablename__ = "item_lists"
#   id: Optional[str] = Field(default=None, primary_key=True)
#   content: str
#   checked: bool = Field(default=False)
#   owner: str = Field(foreign_key="users.id")
#   create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
#   deleted: bool = Field(default=False)
#   delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# class Lists_Items(SQLModel, table=True):
#   __tablename__ = "lists_item"
#   id: Optional[int] = Field(default=None, primary_key=True)
#   content: str
#   checked: bool = Field(default=False)
#   item_list: int = Field(foreign_key="item_lists.id")
#   owner: str = Field(foreign_key="users.id")
#   create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
#   deleted: bool = Field(default=False)
#   delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# class Notes(SQLModel, table=True):
#   __tablename__ = "notes"
#   id: Optional[int] = Field(default=None, primary_key=True)
#   name: str
#   content: str = Field(nullable=False)
#   owner: str = Field(foreign_key="users.id")
#   create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
#   update_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
#   deleted: bool = Field(default=False)
#   delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# class Trips(SQLModel, table=True):
#   __tablename__ = "trips"
#   id: Optional[int] = Field(default=None, primary_key=True)
#   name: str = Field(nullable=False)
#   private: bool = Field(default=False)
#   owner: str = Field(foreign_key="users.id")
#   create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
#   deleted: bool = Field(default=False)
#   delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# class Trips_Dates(SQLModel, table=True):
#   __tablename__ = "trips_dates"
#   id: Optional[int] = Field(default=None, primary_key=True)
#   start_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
#   end_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
#   owner: str = Field(foreign_key="users.id")
#   trip_id: int = Field(foreign_key="trips.id")
#   selected: bool = Field(default=False)
#   create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
#   deleted: bool = Field(default=False)
#   delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# class Trips_Notes_references(SQLModel, table=True):
#   __tablename__ = "trips_notes_references"
#   id: Optional[int] = Field(default=None, primary_key=True)
#   trip_id: int = Field(foreign_key="trips.id")
#   route_id: int = Field(foreign_key="routes.id")

# class Trips_Item_Lists_References(SQLModel, table=True):
#   __tablename__ = "trips_item_lists_references"
#   id: Optional[int] = Field(default=None, primary_key=True)
#   trip_id: int = Field(foreign_key="trips.id")
#   item_list_id: int = Field(foreign_key="item_lists.id")
