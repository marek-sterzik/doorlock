<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;

use App\Auth\UserAuth;
use App\Doorlock\Doorlock;

class MainController extends AbstractController
{
    /** @var UserAuth */
    private $userAuth;

    /** @var Doorlock */
    private $doorlock;

    public function __construct(UserAuth $userAuth, Doorlock $doorlock)
    {
        $this->userAuth = $userAuth;
        $this->doorlock = $doorlock;
    }


    /**
     * @Route("/", name="main")
     */
    public function index(Request $request): Response
    {
        $redirectNeeded = $this->doLoginOrLogout($request);

        if ($redirectNeeded) {
            return $this->redirectToRoute('main');
        }

        $user = $this->userAuth->getLoggedInUser();

        if ($user === null) {
            return $this->render('login.html.twig');
        } else {
            return $this->render('main.html.twig');
        }
    }

    private function doLoginOrLogout(Request $request): bool
    {
        if ($request->getMethod() === 'POST') {
            $login = $request->request->get('login');
            $password = $request->request->get('password');
            
            $success = false;
            if (is_string($login) && is_string($password)) {
                $success = $this->userAuth->loginUser($login, $password);
            }

            if (!$success) {
                $this->userAuth->logoutUser();
            }

            return false;
        } elseif ($request->query->get('logout')) {
            $this->userAuth->logoutUser();

            return true;
        }

        return false;
    }

    /**
     * @Route("/unlock", name="unlock")
     */
    public function unlock(Request $request): Response
    {
        if ($this->userAuth->getLoggedInUser() === null) {
            return $this->redirectToRoute('login');
        }

        $success = $this->doorlock->unlock();
        $responseBody = [
            "code" => $success ? 'ok' : 'error',
        ];
        $responseCode = $success ? 200 : 500;
        return new JsonResponse($responseBody, $responseCode);
    }

    /**
     * @Route("/status", name="status")
     */
    public function status(Request $request): Response
    {
        if ($this->userAuth->getLoggedInUser() === null) {
            return $this->redirectToRoute('login');
        }

        $status = $this->doorlock->getStatus();
        if ($status === null) {
            $status = ["code" => "error"];
        }

        return new JsonResponse($status);
    }
    /**
     * @Route("/prihlaseni", name="login")
     */
    public function login(): Response
    {
        return $this->render('login.html.twig', [
        ]);
    }
    /**
     * @Route("/otevirani", name="open")
     */
    public function open(): Response
    {
        return $this->render('open.html.twig', [
        ]);
    }
}
