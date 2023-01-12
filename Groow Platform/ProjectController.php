<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Project;
use App\ProjectGroup;
use Illuminate\Support\Facades\Auth;
// use Auth;
use App\Message;
use App\Http\Resources\ProjectCollection;
use App\Http\Resources\Project as ProjectResource;
use App\ProjectProcess;
use App\Utils\Utils;
use App\Evidence;
use App\Reflection;
use Illuminate\Support\Facades\Log;
use App\Training;
use App\Training\Subscription;
use Storage;
use Str;
use App\Jobs\CalculateColorProfileForUser;
use Illuminate\Support\Facades\Http;

class ProjectController extends Controller
{

    public function generateProjectFromImage(Request $request, $id)
    {

        $data = $this->validate($request, [
            'image' => 'required|max:100000'
        ]);

        // $request->validate([
        //     'image' => 'required|max:100000'
        // ]);

        if (!$request->hasFile('image')) {
            abort('No image', 422);
        }
        $img = $request->file("image");

        $path = $img->store('images');
        //dd(storage_path($path));
        //make python request
        $client = new \GuzzleHttp\Client();
        $response = $client->post('http://localhost:8080/', [
            'multipart' => [
                [
                    'name' => 'image',
                    'contents' => fopen(str_replace('/', '\\', storage_path('app\\' . $path)), 'r'),
                    // 'Content-type' => 'multipart/form-data',
                ]
            ]
        ]);
        $status = $response->getStatusCode();
        $JSON_STRING = $response->getBody()->getContents();

        // dd($JSON_STRING);

        Log::info('Processing image request', ['json' => $JSON_STRING]);
        // Read bytes of the bod

        $project = Project::create([
            'created_by' => Auth::id(),
            'theme_id' => $id,
            'level_id' => 3,
            'is_public' => 1,
        ]);

        $orderId = 0;

        $json_array = (array)json_decode($JSON_STRING, true);

        foreach ($json_array as $entry) {

            //find token using slug
            if ($entry["type"] == "phases") {
                if ($entry["slug"] == "vertrekpunt") {
                } else if ($entry["slug"] == "eindpunt") {
                } else if ($entry["slug"] == "onbekend") {
                    // dd($entry);
                }

                $id_phase = \App\Phase::where('slug', $entry["slug"])->first()->id;

                $project->process()->create([
                    'process_type' => \App\Phase::class,
                    'process_id' => $id_phase,
                    'order' => $orderId++,
                ]);
            } else if ($entry["type"] == "activities") {

                if ($entry["slug"] == "onbekend") {
                    foreach ($entry["options"] as $option) {
                        if ($option["slug"] == "eindpunt" || $option["slug"] == "vertrekpunt") {
                            //To make sure the process is correctly closed
                            $id_phase = \App\Phase::where('slug', $option["slug"])->first()->id;

                            $project->process()->create([
                                'process_type' => \App\Phase::class,
                                'process_id' => $id_phase,
                                'order' => $orderId++,
                            ]);
                            continue;
                        }

                        //Reliability of each found token can be found in $option["reliability"]
                    }
                }

                $id_activity = \App\Activity::where('slug', $entry["slug"])->first()->id;

                $project->process()->create([
                    'process_type' => \App\Activity::class,
                    'process_id' => $id_activity,
                    'order' => $orderId++,
                ]);
            }
        }
        $project->load('author:id,first_name,last_name', 'members.user', 'process.evidence.author:id,first_name,last_name,avatar');

        return new ProjectResource($project);
    }

    public function updateProjectFromImage(Request $request, $id)
    {
        $project = Project::findOrFail($id);
        $membership = ProjectGroup::where([
            'user_id' => Auth::id(),
            'project_id' => $id,
        ])->count();

        if (Auth::id() != $project->created_by && !$membership) {
            abort(403);
        }

        $project->process()->delete();

        $data = $this->validate($request, [
            'image' => 'required|max:100000',
        ]);

        if (!$request->hasFile('image')) {
            abort('No image', 422);
        }
        $img = $request->file("image");

        $path = $img->store('images');
        //dd(storage_path($path));
        //make python request
        $client = new \GuzzleHttp\Client();
        $response = $client->post('http://ai.prod1.studiotast.com/', [
            //http://ai.prod1.studiotast.com
            'multipart' => [
                [
                    'name' => 'image',
                    'contents' => fopen(str_replace('/', '\\', storage_path('app\\' . $path)), 'r'),
                    'Content-type' => 'multipart/form-data',
                ]
            ]
        ]);
        $status = $response->getStatusCode();
        $JSON_STRING = $response->getBody()->getContents();

        Log::info('Processing image request', ['json' => $JSON_STRING]);
        // Read bytes of the bod

        $orderId = 0;

        $json_array = (array)json_decode($JSON_STRING, true);

        foreach ($json_array as $entry) {

            //find token using slug
            if ($entry["type"] == "phases") {
                if ($entry["slug"] == "vertrekpunt") {
                } else if ($entry["slug"] == "eindpunt") {
                } else if ($entry["slug"] == "onbekend") {
                    // dd($entry);
                }

                $id_phase = \App\Phase::where('slug', $entry["slug"])->first()->id;

                $project->process()->create([
                    'process_type' => \App\Phase::class,
                    'process_id' => $id_phase,
                    'order' => $orderId++,
                ]);
            } else if ($entry["type"] == "activities") {

                if ($entry["slug"] == "onbekend") {
                    foreach ($entry["options"] as $option) {
                        if ($option["slug"] == "eindpunt" || $option["slug"] == "vertrekpunt") {
                            //To make sure the process is correctly closed
                            $id_phase = \App\Phase::where('slug', $option["slug"])->first()->id;

                            $project->process()->create([
                                'process_type' => \App\Phase::class,
                                'process_id' => $id_phase,
                                'order' => $orderId++,
                            ]);
                            continue;
                        }

                        //Reliability of each found token can be found in $option["reliability"]
                    }
                }

                $id_activity = \App\Activity::where('slug', $entry["slug"])->first()->id;

                $project->process()->create([
                    'process_type' => \App\Activity::class,
                    'process_id' => $id_activity,
                    'order' => $orderId++,
                ]);
            }
        }
        $project->load('author:id,first_name,last_name', 'members.user', 'process.evidence.author:id,first_name,last_name,avatar');

        return new ProjectResource($project);
    }
}
