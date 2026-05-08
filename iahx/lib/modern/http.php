<?php

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Symfony\Component\Routing\Exception\ResourceNotFoundException;
use Symfony\Component\Routing\Matcher\UrlMatcher;
use Symfony\Component\Routing\RequestContext;
use Symfony\Component\Routing\Route;
use Symfony\Component\Routing\RouteCollection;

class IahxModernApplication implements ArrayAccess {
    private $routes;
    private $services;

    public function __construct(array $services = array()) {
        $this->routes = new RouteCollection();
        $this->services = $services;
    }

    public function get($path, $controller) {
        return $this->addRoute($path, $controller, array('GET'));
    }

    public function post($path, $controller) {
        return $this->addRoute($path, $controller, array('POST'));
    }

    public function match($path, $controller) {
        return $this->addRoute($path, $controller);
    }

    public function handle(Request $request) {
        $this->services['request'] = $request;
        $context = new RequestContext();
        $context->fromRequest($request);

        try {
            $attributes = (new UrlMatcher($this->routes, $context))->match($request->getPathInfo());
        } catch (ResourceNotFoundException $exception) {
            throw new NotFoundHttpException('No route found for "' . $request->getPathInfo() . '".', $exception);
        }

        $controller = $attributes['_controller'];
        unset($attributes['_controller'], $attributes['_route']);

        return $this->toResponse($this->invoke($controller, $request, $attributes));
    }

    public function run(?Request $request = null) {
        $response = $this->handle($request ?: Request::createFromGlobals());
        $response->send();
    }

    public function offsetExists($offset): bool {
        return array_key_exists($offset, $this->services);
    }

    public function offsetGet($offset): mixed {
        return $this->services[$offset];
    }

    public function offsetSet($offset, $value): void {
        $this->services[$offset] = $value;
    }

    public function offsetUnset($offset): void {
        unset($this->services[$offset]);
    }

    private function addRoute($path, $controller, array $methods = array()) {
        $route = new Route($this->normalizePath($path), array('_controller' => $controller));
        if ($methods) {
            $route->setMethods($methods);
        }

        $this->routes->add('route_' . count($this->routes), $route);

        return new IahxModernRoute($route);
    }

    private function normalizePath($path) {
        if ($path === '') {
            return '/';
        }

        return '/' . ltrim($path, '/');
    }

    private function invoke($controller, Request $request, array $attributes) {
        $arguments = array($request);

        foreach ($this->controllerParameters($controller) as $index => $parameter) {
            if ($index === 0) {
                continue;
            }

            $name = $parameter->getName();
            $arguments[] = array_key_exists($name, $attributes) ? $attributes[$name] : null;
        }

        ob_start();
        try {
            $result = call_user_func_array($controller, $arguments);
            $output = ob_get_clean();
        } catch (Throwable $exception) {
            ob_end_clean();
            throw $exception;
        }

        if ($result === null && $output !== '') {
            return $output;
        }

        return $result;
    }

    private function controllerParameters($controller) {
        if ($controller instanceof Closure) {
            return (new ReflectionFunction($controller))->getParameters();
        }

        if (is_array($controller)) {
            return (new ReflectionMethod($controller[0], $controller[1]))->getParameters();
        }

        if (is_string($controller) && strpos($controller, '::') !== false) {
            return (new ReflectionMethod($controller))->getParameters();
        }

        return (new ReflectionFunction($controller))->getParameters();
    }

    private function toResponse($result) {
        if ($result instanceof Response) {
            return $result;
        }

        return new Response((string) $result);
    }
}

function iahx_modern_create_application(array $services = array()) {
    return new IahxModernApplication($services);
}

class IahxModernRoute {
    private $route;

    public function __construct(Route $route) {
        $this->route = $route;
    }

    public function value($variable, $default) {
        $this->route->setDefault($variable, $default);

        return $this;
    }

    public function getRoute() {
        return $this->route;
    }
}
