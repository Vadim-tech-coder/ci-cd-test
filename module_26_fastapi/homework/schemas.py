from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    title_of_dish: str = Field(..., description="Название блюда", example="Макароны по флотски")
    description: str = Field(..., description="Описание рецепта", example="Блюдо из макарон и фарша")
    ingredients: str = Field(..., description="Ингредиенты, разделенные запятыми", example="Фарш, макароны, соль")
    preparing_time_in_min: int = Field(..., ge=1, description="Время приготовления в минутах", example=60)
    view_count: int = Field(..., description="Количество просмотров рецепта, увеличивается при просмотре рецепта", example=5)

class RecipeIn(BaseRecipe):
    ...

class OneRecipeOut(BaseModel):
    title_of_dish: str = Field(..., description="Название блюда", example="Макароны по флотски")
    description: str = Field(..., description="Описание рецепта", example="Блюдо из макарон и фарша")
    ingredients: str = Field(..., description="Ингредиенты, разделенные запятыми", example="Фарш, макароны, соль")
    preparing_time_in_min: int = Field(..., ge=1, description="Время приготовления в минутах", example=60)


    class Config:
        orm_mode = True

class ListRecipeOut(BaseModel):
    title_of_dish: str = Field(..., description="Название блюда", example="Макароны по флотски")
    view_count: int = Field(..., description="Количество просмотров рецепта, увеличивается при просмотре рецепта", example=5)
    preparing_time_in_min: int = Field(..., ge=1, description="Время приготовления в минутах", example=60)

    class Config:
        orm_mode = True

class RecipeOut(BaseRecipe):
    id: int =  Field(..., description="Уникальный идентификатор рецепта", example=123)

    class Config:
        orm_mode = True
