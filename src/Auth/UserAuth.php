<?php

namespace App\Auth;

use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\HttpFoundation\RequestStack;
use App\Repository\UserRepository;
use App\Entity\User;

class UserAuth
{
    /** @var SessionInterface */
    private $session;

    /** @var UserRepository */
    private $userRepository;

    /** @var PasswordVerifier */
    private $passwordVerifier;

    public function __construct(
        SessionInterface $session,
        UserRepository $userRepository
    ) {
        $this->session = $session;
        $this->userRepository = $userRepository;
    }

    public function loginUser(string $username, string $password): bool
    {
        $this->session->set("admin-user-id", null);
        $user = $this->getUserByUsernameAndPassword($username, $password);
        if ($user === null) {
            return false;
        }
        $userId = $user->getId();
        if ($userId === null) {
            $userId = -1;
        }
        $this->session->set("admin-user-id", $userId);
        return true;
    }

    private function logoutUser(): void
    {
        $this->session->set("admin-user-id", null);
    }

    public function getLoggedInUser(): ?User
    {
        $userId = $this->session->get("admin-user-id");
        if ($userId === null) {
            return null;
        }
        if ($userId < 0) {
            return null;
        }

        return $this->userRepository->find($userId);
    }

    private function getUserByUsernameAndPassword(string $username, string $password): ?User
    {
        $user = $this->userRepository->findOneBy(['login' => $username]);
        if ($user === null) {
            return null;
        }
        if (!$password === $user->getPassword()) {
            return null;
        }
        return $user;
    }
}
