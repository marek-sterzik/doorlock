<?php

namespace App\Doorlock;

/**
 * @author František Hrdý
 * @author Martin Růžek
 */
class Doorlock
{
    /**
     * @var string
     */
    private $lockUrl;

    /**
     * @var string
     */
    private $lockAuthenticationKey;

    /**
     * @param string $lockUrl
     * @param string $lockAuthenticationKey
     */
    public function __construct(string $lockUrl, string $lockAuthenticationKey)
    {
        $this->lockUrl = $this->canonizeUrl($lockUrl);
        $this->lockAuthenticationKey = $lockAuthenticationKey;
    }

    public function unlock(): bool
    {
        $data = $this->makeRequest("/open");
        return isset($data['code']) && ($data['code'] === 'ok');
    }

    public function getStatus(): ?array
    {
        return $this->makeRequest("/status");
    }

    private function canonizeUrl(string $url): string
    {
        return rtrim($url, '/');
    }

    private function makeRequest(string $path): ?array
    {
        $url = $this->lockUrl . $path . "?sid=" . urlencode($this->lockAuthenticationKey);
        $data = @file_get_contents($url);
        if (!is_string($data)) {
            return null;
        }

        $data = @json_decode($data, true);

        if (!is_array($data)) {
            return null;
        }

        return $data;
    }
}
