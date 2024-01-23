from typing import Optional

from sqlmodel import Field, SQLModel, JSON

from datetime import datetime

import utcnow as utcnow


class users(SQLModel, table=True):
  id: Optional[str] = Field(default=None, primary_key=True)
  first_name: str = Field(nullable=False)
  last_name: str = Field(nullable=False)
  email: str = Field(nullable=False)
  auth_method: Optional[str] = Field(default=None)
  password: Optional[str] = Field(default=None)
  private: bool = Field(default=False)
  create_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  deleted: bool = Field(default=False)
  delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class routes(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  route: JSON
  route_history: JSON
  name: str
  comment: str
  owner: str = Field(foreign_key="users.id")
  create_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  deleted: bool = Field(default=False)
  delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class item_lists(SQLModel, table=True):
  id: Optional[str] = Field(default=None, primary_key=True)
  content: str
  checked: bool = Field(default=False)
  owner: str = Field(foreign_key="users.id")
  create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
  deleted: bool = Field(default=False)
  delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class lists_items(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  content: str
  checked: bool = Field(default=False)
  item_list: int = Field(foreign_key="item_lists.id")
  owner: str = Field(foreign_key="users.id")
  create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
  deleted: bool = Field(default=False)
  delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class notes(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str
  content: str = Field(nullable=False)
  owner: str = Field(foreign_key="users.id")
  create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
  update_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
  deleted: bool = Field(default=False)
  delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class trips(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str = Field(nullable=False)
  private: bool = Field(default=False)
  owner: str = Field(foreign_key="users.id")
  create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
  deleted: bool = Field(default=False)
  delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class trips_dates(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  start_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  end_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  owner: str = Field(foreign_key="users.id")
  trip_id: int = Field(foreign_key="trips.id")
  selected: bool = Field(default=False)
  create_time: datetime = Field(default_factory=datetime.utcnow,  nullable=False)
  deleted: bool = Field(default=False)
  delete_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class trips_notes_references(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  trip_id: int = Field(foreign_key="trips.id")
  route_id: int = Field(foreign_key="routes.id")

class trips_item_lists_references(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  trip_id: int = Field(foreign_key="trips.id")
  item_list_id: int = Field(foreign_key="item_lists.id")
