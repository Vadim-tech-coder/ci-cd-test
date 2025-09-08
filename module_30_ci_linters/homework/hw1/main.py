from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import schemas
from database import engine, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняющийся при старте приложения
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # Код, выполняющийся при завершении приложения
    session = Depends(get_session)
    await session.close()
    await engine.dispose()


app = FastAPI(
    title="Recepi API",
    description="API для работы с рецептами",
    version="1.0",
    lifespan=lifespan,
)

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(models.Base.metadata.create_all)


# @app.on_event("shutdown")
# async def shutdown(session: AsyncSession = Depends(get_session)):
#     await session.close()
#     await engine.dispose()


@app.post(
    "/recipes/",
    response_model=schemas.RecipeOut,
    status_code=201,
    summary="Создать новый рецепт",
    description="Создает новый рецепт на основе введенных данных",
)
async def add_recipe(
    recipe: schemas.RecipeIn, session: AsyncSession = Depends(get_session)  # noqa
) -> models.Recipe:
    """
    Создает рецепт и возвращает его с присвоенным ID и начальным view_count = 0
    """
    new_recipe = models.Recipe(**recipe.model_dump())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe


@app.get(
    "/recipes/",
    response_model=List[schemas.ListRecipeOut],
    summary="Получить список всех рецептов",
    description="Возвращает список всех рецептов, "
                "отсортированных по количеству просмотров "
                "и времени приготовления.",
)
async def get_recipes(
    session: AsyncSession = Depends(get_session),  # noqa
) -> List[models.Recipe]:
    """
    Функция делает запрос в БД всех рецептов и возвращает список рецептов.
    """
    stmt = select(models.Recipe).order_by(
        models.Recipe.view_count.desc(),
        models.Recipe.preparing_time_in_min.asc()
    )
    res = await session.execute(stmt)
    return list(res.scalars().all())


@app.get(
    "/recipes/{idx}",
    response_model=schemas.OneRecipeOut,
    summary="Получить рецепт по ID",
    description="Возвращает рецепт по уникальному идентификатору",
)
async def get_recipe_by_id(
    idx: int = Path(..., description="Уникальный идентификатор рецепта", ge=1),  # noqa
    session: AsyncSession = Depends(get_session),  # noqa
):
    """
    Функция делает выборку из БД по уникальному ID рецепта.
    Если рецепт найден, то увеличивает значение в колонке view_count.
    """
    stmt = select(models.Recipe).where(models.Recipe.id == idx)
    res = await session.execute(stmt)
    record = res.scalars().first()  # кортеж из полей или None

    if record is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    views = record.view_count + 1
    upd_stmt = (
        update(models.Recipe).where(models.Recipe.id == idx).
        values(view_count=views)
    )
    await session.execute(upd_stmt)
    await session.commit()
    return record
