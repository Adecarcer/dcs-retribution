from fastapi import APIRouter, Depends, HTTPException, status

from game import Game
from game.server import GameContext
from .models import MapZonesJs
from ..leaflet import ShapelyUtil

router: APIRouter = APIRouter(prefix="/map-zones")


@router.get("/")
def get(game: Game = Depends(GameContext.get)) -> MapZonesJs:
    zones = game.theater.landmap
    if zones is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return MapZonesJs(
        inclusion=ShapelyUtil.polys_to_leaflet(zones.inclusion_zones, game.theater),
        exclusion=ShapelyUtil.polys_to_leaflet(zones.exclusion_zones, game.theater),
        sea=ShapelyUtil.polys_to_leaflet(zones.sea_zones, game.theater),
    )
