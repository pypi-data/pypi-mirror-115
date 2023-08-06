from pollination.honeybee_radiance.raytrace import RayTracingDaylightFactor, \
    RayTracingPointInTime, RayTracingViewPercent
from queenbee.plugin.function import Function


def test_ray_tracing_daylight_factor():
    function = RayTracingDaylightFactor().queenbee
    assert function.name == 'ray-tracing-daylight-factor'
    assert isinstance(function, Function)


def test_ray_tracing_point_in_time():
    function = RayTracingPointInTime().queenbee
    assert function.name == 'ray-tracing-point-in-time'
    assert isinstance(function, Function)


def test_ray_tracing_view_percent():
    function = RayTracingViewPercent().queenbee
    assert function.name == 'ray-tracing-view-percent'
    assert isinstance(function, Function)
