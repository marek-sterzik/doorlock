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
    private $unlockUrl;

    /**
     * @var string
     */
    private $lockStatusRequest;

    /**
     * @var string
     */
    private $authentication;

    /**
     * @param string $unlockUrl
     * @param string $lockStatusRequest
     * @param string $authentication
     */
    public function __construct(string $unlockUrl, string $lockStatusRequest, string $authentication)
    {
        $this->unlockUrl = $unlockUrl;
        $this->lockStatusRequest = $lockStatusRequest;
        $this->authentication = $authentication;
    }

    public function unlock(): void
    {
        header('Location: ' . $this->unlockUrl);
        die;
    }

    public function getStatus(): array
    {
        $authentication = base64_encode($this->authentication);
        $context = stream_context_create([
            'http' => [
                'header' => 'Authorization: Basic ' . $authentication
            ]
        ]);
        $rawStatus = @file_get_contents($this->lockStatusRequest, false, $context);
        if ($rawStatus === false) {
            throw new Exception('An attempt to retrieve lock status failed.');
        }
        // Example: $rawStatus = 'true-600' | $rawStatus = 'false-null'
        $status = explode('-', $rawStatus);

        $finalStatus = [];

        if ($status[0] === 'true') {
            $finalStatus['state'] = true;
            $finalStatus['time_to_lock'] = (int)$status[1];
        } else {
            $finalStatus['state'] = false;
            $finalStatus['time_to_lock'] = null;
        }
            
        return $finalStatus;
    }
}
