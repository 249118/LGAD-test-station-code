from imports import *
from application import *

def main():
    #initialise imgui and glfw
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    #initialise application object
    app = Application()

    #main render loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        io = imgui.get_io()
        imgui.new_frame()
        imgui.begin("FPS", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        imgui.text("FPS: " + str(int(io.framerate)))
        imgui.end()

        #run main app GUI
        app.run()

        gl.glClearColor(0., 0., 0., 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    #deinitialise application and quit
    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    #helper function for glfw initialisation 
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.MAXIMIZED, glfw.TRUE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


if __name__ == "__main__":
    main()