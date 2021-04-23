<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;

class MainController extends AbstractController
{
    /**
     * @Route("/", name="main")
     */
    public function index(): Response
    {
        return $this->render('main.html.twig', [
        ]);
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
