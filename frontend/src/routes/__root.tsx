import { createRootRoute, Outlet } from "@tanstack/react-router"
import Header from "@/components/Common/Header"
import NotFound from "@/components/Common/NotFound"

export const Route = createRootRoute({
  component: () => (
    <>
      <Header />
      <Outlet />
    </>
  ),
  notFoundComponent: () => <NotFound />,
})
