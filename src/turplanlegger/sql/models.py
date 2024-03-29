import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import BOOLEAN, TEXT
from sqlalchemy.sql import false
from sqlmodel import Field, SQLModel


class UserBase(SQLModel, table=False):
    """User base SQLModel
    This class is used for validation.
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

    first_name: str = Field(sa_column=Column(type_=TEXT, nullable=False))
    last_name: str = Field(sa_column=Column(type_=TEXT, nullable=False))
    email: str = Field(sa_column=Column(type_=TEXT, nullable=False))
    private: bool = Field(
        default=False, sa_column=Column(type_=BOOLEAN, default=False, server_default=false(), nullable=False)
    )


class User(UserBase, table=True):
    """User table SQLModel
    This class is for SQLAlchemy
    """

    __tablename__ = 'users'
    id: uuid.UUID = Field(
        default=uuid.uuid4(), primary_key=True, index=True, nullable=False, description='ID of the user as UUID'
    )
    create_time: datetime = Field(
        default=datetime.now(UTC),
        sa_column=Column(
            type_=DateTime, default=datetime.now(UTC), server_default=func.current_timestamp(), nullable=False
        ),
    )
    deleted: bool = Field(
        default=False, sa_column=Column(type_=BOOLEAN, default=False, server_default=false(), nullable=False)
    )
    delete_time: datetime | None = Field(default=None)


class UserCreate(UserBase, table=False):
    """User table SQLModel
    This class is when creating a new user
    """

    id: uuid.UUID = Field(
        default=uuid.uuid4(), primary_key=True, index=True, nullable=False, description='ID of the user as UUID'
    )


class UserRead(UserBase, table=False):
    """User table SQLModel
    This class is when creating a new user
    """

    id: uuid.UUID
    create_time: datetime
    deleted: bool
    delete_time: Optional[datetime]


class UserUpdate(UserBase, table=False):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]  # Should this be updateable?
    private: Optional[bool]


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
