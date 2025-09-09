from pydantic import BaseModel, ConfigDict, Field


class BaseRecipe(BaseModel):
    title_of_dish: str = Field(
        ...,
        description="Название блюда",
        json_schema_extra={"example": "Макароны по флотски"},
    )
    description: str = Field(
        ...,
        description="Описание рецепта",
        json_schema_extra={"example": "Блюдо из макарон и фарша"},
    )
    ingredients: str = Field(
        ...,
        description="Ингредиенты, разделенные запятыми",
        json_schema_extra={"example": "Фарш, макароны, соль"},
    )
    preparing_time_in_min: int = Field(
        ...,
        ge=1,
        description="Время приготовления в минутах",
        json_schema_extra={"example": 60},
    )
    view_count: int = Field(
        ...,
        description="Количество просмотров рецепта, "
        "увеличивается при просмотре рецепта",
        json_schema_extra={"example": 5},
    )

    model_config = ConfigDict(from_attributes=True)


class RecipeIn(BaseRecipe): ...


class OneRecipeOut(BaseModel):
    title_of_dish: str = Field(
        ...,
        description="Название блюда",
        json_schema_extra={"example": "Макароны по флотски"},
    )
    description: str = Field(
        ...,
        description="Описание рецепта",
        json_schema_extra={"example": "Блюдо из макарон и фарша"},
    )
    ingredients: str = Field(
        ...,
        description="Ингредиенты, разделенные запятыми",
        json_schema_extra={"example": "Фарш, макароны, соль"},
    )
    preparing_time_in_min: int = Field(
        ...,
        ge=1,
        description="Время приготовления в минутах",
        json_schema_extra={"example": 60},
    )

    model_config = ConfigDict(from_attributes=True)


class ListRecipeOut(BaseModel):
    title_of_dish: str = Field(
        ...,
        description="Название блюда",
        json_schema_extra={"example": "Макароны по флотски"},
    )
    view_count: int = Field(
        ...,
        description="Количество просмотров рецепта, "
        "увеличивается при просмотре рецепта",
        json_schema_extra={"example": 5},
    )
    preparing_time_in_min: int = Field(
        ...,
        ge=1,
        description="Время приготовления в минутах",
        json_schema_extra={"example": 60},
    )

    model_config = ConfigDict(from_attributes=True)


class RecipeOut(BaseRecipe):
    id: int = Field(
        ...,
        description="Уникальный идентификатор рецепта",
        json_schema_extra={"example": 123},
    )

    model_config = ConfigDict(from_attributes=True)
