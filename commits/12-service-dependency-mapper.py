"""Map direct and transitive dependencies for a service."""


def resolve_dependencies(service: str, graph: dict, seen=None) -> set:
    seen = seen or set()
    if service in seen:
        return seen
    seen.add(service)
    for dep in graph.get(service, []):
        resolve_dependencies(dep, graph, seen)
    return seen


if __name__ == "__main__":
    g = {"api": ["db", "cache"], "cache": ["redis"]}
    deps = resolve_dependencies("api", g)
    assert "redis" in deps
    print("service_dependency_mapper: ok")
