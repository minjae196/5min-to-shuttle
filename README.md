{
"event": "Configuration file loaded: /home/adminuser/venv/lib/python3.11/site-packages/readmeai/config/settings/ignore_list.toml",
"level": "info",
"logger": "readmeai.config.settings",
"timestamp": "2024-12-02T07:20:43.074157Z",
"filename": "settings.py",
"func_name": "_load_settings",
"lineno": 276
}
{
"event": "Configuration file loaded: /home/adminuser/venv/lib/python3.11/site-packages/readmeai/config/settings/languages.toml",
"level": "info",
"logger": "readmeai.config.settings",
"timestamp": "2024-12-02T07:20:43.074995Z",
"filename": "settings.py",
"func_name": "_load_settings",
"lineno": 276
}
{
"event": "Configuration file loaded: /home/adminuser/venv/lib/python3.11/site-packages/readmeai/config/settings/parsers.toml",
"level": "info",
"logger": "readmeai.config.settings",
"timestamp": "2024-12-02T07:20:43.075771Z",
"filename": "settings.py",
"func_name": "_load_settings",
"lineno": 276
}
{
"event": "Configuration file loaded: /home/adminuser/venv/lib/python3.11/site-packages/readmeai/config/settings/prompts.toml",
"level": "info",
"logger": "readmeai.config.settings",
"timestamp": "2024-12-02T07:20:43.076902Z",
"filename": "settings.py",
"func_name": "_load_settings",
"lineno": 276
}
{
"event": "Configuration file loaded: /home/adminuser/venv/lib/python3.11/site-packages/readmeai/config/settings/tool_config.toml",
"level": "info",
"logger": "readmeai.config.settings",
"timestamp": "2024-12-02T07:20:43.083142Z",
"filename": "settings.py",
"func_name": "_load_settings",
"lineno": 276
}
{
"event": "Configuration file loaded: /home/adminuser/venv/lib/python3.11/site-packages/readmeai/config/settings/tooling.toml",
"level": "info",
"logger": "readmeai.config.settings",
"timestamp": "2024-12-02T07:20:43.084932Z",
"filename": "settings.py",
"func_name": "_load_settings",
"lineno": 276
}
{
"event": "Pydantic settings: dict_keys(['config', 'ignore_list', 'languages', 'parsers', 'prompts', 'tool_config', 'tooling'])",
"level": "info",
"logger": "readmeai.cli.main",
"timestamp": "2024-12-02T07:20:43.086940Z",
"filename": "main.py",
"func_name": "main",
"lineno": 86
}
{
"event": "Repository settings: repository='https://github.com/eli64s/readme-aihttps://github.com/minjae196/5min-to-shuttle' full_name='eli64s/readme-aihttps:' host_domain='github.com' host='github' name='5min-to-shuttle'",
"level": "info",
"logger": "readmeai.cli.main",
"timestamp": "2024-12-02T07:20:43.087168Z",
"filename": "main.py",
"func_name": "main",
"lineno": 87
}
{
"event": "LLM API settings: api='OPENAI' base_url='https://api.openai.com/v1/chat/completions' context_window=3900 encoder='cl100k_base' host_name=Url('https://api.openai.com/') localhost=Url('http://localhost:11434/') model='gpt-3.5-turbo' path='v1/chat/completions' temperature=0.1 tokens=699 top_p=0.9",
"level": "info",
"logger": "readmeai.cli.main",
"timestamp": "2024-12-02T07:20:43.087368Z",
"filename": "main.py",
"func_name": "main",
"lineno": 88
}
{
"event": "Failed to clone repository https://github.com/eli64s/readme-aihttps://github.com/minjae196/5min-to-shuttle: Cmd('git') failed due to: exit code(128)\n  cmdline: git clone -v --depth=1 --single-branch -- https://github.com/eli64s/readme-aihttps://github.com/minjae196/5min-to-shuttle /tmp/tmp7uzxf082\n  stderr: 'Cloning into '/tmp/tmp7uzxf082'...\nremote: Not Found\nfatal: repository 'https://github.com/eli64s/readme-aihttps://github.com/minjae196/5min-to-shuttle/' not found\n'",
"level": "error",
"logger": "readmeai.readers.git.repository",
"timestamp": "2024-12-02T07:20:43.278418Z",
"filename": "repository.py",
"func_name": "load_data",
"lineno": 72
}
Traceback (most recent call last):
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/readers/git/repository.py", line 61, in load_data
await clone_repository(str(repository), temp_dir_path)
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/readers/git/repository.py", line 24, in clone_repository
await loop.run_in_executor(
File "/home/adminuser/.local/share/uv/python/cpython-3.11.10-linux-x86_64-gnu/lib/python3.11/concurrent/futures/thread.py", line 58, in run
result = self.fn(*self.args, **self.kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/readers/git/repository.py", line 26, in <lambda>
lambda: git.Repo.clone_from(
^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/git/repo/base.py", line 1525, in clone_from
return cls._clone(
^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/git/repo/base.py", line 1396, in _clone
finalize_process(proc, stderr=stderr)
File "/home/adminuser/venv/lib/python3.11/site-packages/git/util.py", line 504, in finalize_process
proc.wait(**kwargs)
File "/home/adminuser/venv/lib/python3.11/site-packages/git/cmd.py", line 834, in wait
raise GitCommandError(remove_password_if_present(self.args), status, errstr)
git.exc.GitCommandError: Cmd('git') failed due to: exit code(128)
cmdline: git clone -v --depth=1 --single-branch -- https://github.com/eli64s/readme-aihttps://github.com/minjae196/5min-to-shuttle /tmp/tmp7uzxf082
stderr: 'Cloning into '/tmp/tmp7uzxf082'...
remote: Not Found
fatal: repository 'https://github.com/eli64s/readme-aihttps://github.com/minjae196/5min-to-shuttle/' not found
'
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/__main__.py", line 32, in error_handler
yield
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/__main__.py", line 40, in readme_agent
asyncio.run(readme_generator(config, output_file))
File "/home/adminuser/.local/share/uv/python/cpython-3.11.10-linux-x86_64-gnu/lib/python3.11/asyncio/runners.py", line 190, in run
return runner.run(main)
^^^^^^^^^^^^^^^^
File "/home/adminuser/.local/share/uv/python/cpython-3.11.10-linux-x86_64-gnu/lib/python3.11/asyncio/runners.py", line 118, in run
return self._loop.run_until_complete(task)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/.local/share/uv/python/cpython-3.11.10-linux-x86_64-gnu/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
return future.result()
^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/__main__.py", line 46, in readme_generator
repo_path = await load_data(config.config.git.repository, temp_dir)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/readers/git/repository.py", line 73, in load_data
raise GitCloneError(
readmeai.errors.GitCloneError: Failed to clone repository: Failed to clone repository https://github.com/eli64s/readme-aihttps://github.com/minjae196/5min-to-shuttle
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
File "/home/adminuser/venv/bin/readmeai", line 8, in <module>
sys.exit(main())
^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
return self.main(*args, **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/click/core.py", line 1078, in main
rv = self.invoke(ctx)
^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
return ctx.invoke(self.callback, **ctx.params)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/click/core.py", line 783, in invoke
return __callback(*args, **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/cli/main.py", line 90, in main
readme_agent(config=config, output_file=output)
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/__main__.py", line 39, in readme_agent
with error_handler():
File "/home/adminuser/.local/share/uv/python/cpython-3.11.10-linux-x86_64-gnu/lib/python3.11/contextlib.py", line 158, in __exit__
self.gen.throw(typ, value, traceback)
File "/home/adminuser/venv/lib/python3.11/site-packages/readmeai/__main__.py", line 34, in error_handler
raise ReadmeGeneratorError(e) from e
readmeai.errors.ReadmeGeneratorError: Error generating README: Failed to clone repository: Failed to clone repository https://github.com/eli64s/readme-aihttps://github.com/minjae196/5min-to-shuttle
